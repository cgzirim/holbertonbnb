#!/usr/bin/env python3
"""Fabfile to deploy HolbertonBnB to web servers

Run `fab --list` to list all available commands.

Usage:
    `fab <script> --<option>=<value>`
Options:
    deploy_loadbalancer - Configures an Ubuntu server to distribute traffic
                          to specified webservers.
    pack --folder=STR - Creates a tar archive.
    upload --archive=STR - Distributes a tar archive.
    setup_webservers - Installs and configures Nginx on an Ubuntu server.
    start_apps - Starts the application servers.
    deploy_webservers - runs pack(), upload(), setup_webservers(),
                        and start_apps on specified Ubuntu servers.
"""
import datetime
from fabric.api import *
from os.path import isdir
from os.path import exists
from fabric.contrib import files
from invoke.exceptions import UnexpectedExit


env.roledefs = {
    "web_server": ["ubuntu@ec2-18-206-203-208.compute-1.amazonaws.com"],
    "web_servers": [
        "ubuntu@ec2-52-90-233-183.compute-1.amazonaws.com",
        "ubuntu@ec2-44-204-36-60.compute-1.amazonaws.com",
    ],
    "load_balancer": ["ubuntu@ec2-52-90-233-183.compute-1.amazonaws.com"],
}

domain_name = "miniairbnb.gq"
subdomain_name = "www.miniairbnb.gq"


@roles("load_balancer")
def deploy_loadbalancer():
    """Configures an Ubuntu server to distribute incoming request to servers
    specified in env.roledef['web_servers'] using HAproxy.
    It configures HAproxy to
        - accept encrypted SSL traffic for the subdomain 'www.' on TCP port 443
        - automatically redirect HTTP traffic to HTTPS
        - distribute traffic to available web servers using roundrobin
          algorithm
    """
    sudo("apt-get update")

    # Obtain a certificate using certbot
    sudo("apt-get install certbot")

    try:  # ensure port 80 is open
        sudo("kill $(lsof -t -i:80)")
    except:
        pass

    sudo(
        f"certbot certonly\
        --standalone --preferred-challenges http\
        --http-01-port 80 -d {domain_name} -d www.{domain_name}"
    )
    sudo("mkdir -p /etc/haproxy/certs")
    sudo(
        f"DOMAIN='miniairbnb.gq' sudo -E bash -c\
        'cat /etc/letsencrypt/live/$DOMAIN/fullchain.pem\
        /etc/letsencrypt/live/$DOMAIN/privkey.pem >\
        /etc/haproxy/certs/$DOMAIN.pem'"
    )
    sudo("chmod -R go-rwx /etc/haproxy/certs")

    # Configure HAproxy

    sudo("apt-get install haproxy")
    haproxy_config = """
    global
        log     /dev/log local0
        maxconn 2048
        user haproxy
        group haproxy
        tune.ssl.default-dh-param 2048

    defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        retries 3
        option redispatch
        timeout connect  5000
        timeout client  10000
        timeout server  10000
        option  forwardfor
        option  http-server-close

    frontend www-http
        bind 0.0.0.0:90
        http-request set-header X-Forwarded-Proto http
        default_backend www-backend
        redirect scheme https code 301 if !{{ ssl_fc }}

    frontend www-https
        bind 0.0.0.0:443 ssl crt /etc/haproxy/certs/{domain}.pem
        http-request set-header X-Forwarded-Proto https
        acl letsencrypt-acl path_beg /.well-known/acme-challenge/
        use_backend letsencrypt-backend if letsencrypt-acl
        default_backend www-backend
        option http-server-close

    backend www-backend
        balance  roundrobin
        redirect scheme https if !{{ ssl_fc }}
        server 1982-web-01 {ip_addr_1}:80 check
        server 1982-web-02 {ip_addr_2}:80 check
        option httpchk

    backend letsencrypt-backend
        server letsencrypt 127.0.0.1:54321
    """

    haproxy_config = haproxy_config.format(
        domain=domain_name,
        # ip_addr_1=env.roledefs['web_servers'][0]
        # ip_addr_2=env.roledefs['web_servers'][1]
        ip_addr_1="52.90.233.183",
        ip_addr_2="44.204.36.60",
    )

    sudo(f'printf %s "{haproxy_config}" > /etc/haproxy/haproxy.cfg')
    sudo("service haproxy restart")


def pack(folder):
    """Generates a .tgz archive from the contents of the specified folder in
    the Holbertonbnb repo.

    Packs the folder in the format `versions/{folder}-{date}.tgz`.

    Args:
        folder (str): The name of folder to pack
    """
    if isdir("versions") is False:
        local("sudo mkdir -p versions")

    time = datetime.datetime.now()
    file_name = "versions/{}-{}{}{}{}{}{}.tgz".format(
        folder, time.year,
        time.month,
        time.day, time.hour,
        time.minute, time.second
    )

    local(f"sudo tar -czvf {file_name} {folder}")
    print("done.")
    return file_name


def upload(archive):
    """Distributes an archive to a specified web server.

    Expects an archive in the format `versions/{folder}-{date}.tgz`.

    Argument:
        archive_path (str): Name of the archive to distribute
    """
    if exists(archive) is False:
        return

    put(archive, "/tmp/")

    # Uncompress the archive to the folder
    # /data/<archive filename without extension> on the web server
    archive_file = archive[archive.index("/") + 1:]
    folder_name = archive_file.split("-")[0]

    if files.exists(f"/data/{folder_name}"):
        print(f"/data/{folder_name} exists. ", end="")
        ans = input("Do you want to overwrite this file? [Y/n]: ")

        if ans.lower() == "y":
            print("Overwriting... ")
            run(f"sudo rm -rf /data/{folder_name}")
        else:
            return

    run(f"sudo mkdir -p /data/{folder_name}/")
    run(f"sudo tar -xzf /tmp/{archive_file} -C /data/{folder_name}")

    run(f"sudo rm /tmp/{archive_file}")

    run(f"sudo mv /data/{folder_name}/{folder_name}/* /data/{folder_name}")
    run(f"sudo rm -rf /data/{folder_name}/{folder_name}")
    print("done.")


def pack_and_upload(folder):
    """Generates an archive from a folder and distributes it
    to a server.

    Args:
        folder (str): The name of the folder to pack and upload.
    """
    archive = pack(folder)
    upload(archive)


def setup_webserver():
    """Configures Nginx and installs the necessary modules on an Ubuntu
    machine to serve Holbertonbnb.
    """
    run("sudo apt-get update")
    run("sudo apt-get install nginx")

    nginx_config = """
    server {
        listen 80;
        listen [::]:80;

        # Use server IP as domain name
        server_name $(dig +short myip.opendns.com @resolver1.opendns.com);

        # Customize HTTP response header
        add_header  X-Served-By $HOSTNAME;

        location / {
            proxy_pass http://127.0.0.1:5000/hbnb;
        }

        location /api {
            proxy_pass http://127.0.0.1:5001/api;
        }

        # Serve static content for Mini_AirBnB
        location /static {
            proxy_pass http://127.0.0.1:5000;
        }

        # 404 error page
        error_page 404 /404.html;
        location /404 {
            root /var/www/html;
            internal;
        }
    }
    """

    sudo(f'printf %s "{nginx_config}" > /etc/nginx/sites-available/default')

    run("sudo ufw allow 'Nginx Full'")
    run("sudo service nginx restart")

    put("requirements.txt", "/data/", use_sudo=True)
    sudo("apt-get install mysql-server")
    sudo("apt-get install default-libmysqlclient-dev")
    sudo("apt-get install python3-pip")
    sudo("pip3 install -r /data/requirements.txt")


def start_apps():
    """Starts Holbertonbnb WSGI apps."""
    print("Starting Gunicorn instances... ")
    try:
        run("kill $(lsof -t -i:5000)")
        run("kill $(lsof -t -i:5001)")
    except:
        pass

    # Run the gunicorn instances in the background
    sudo(f"gunicorn --chdir /data/ --bind 0.0.0.0:5000 web_flask.hbnb:app -- daemon &")
    sudo(f"gunicorn --chdir /data/ --bind 0.0.0.0:5001 api.v1.app:app --daemon &")
    print("Application servers activated!")


@roles("web_servers")
def deploy_webservers(folder="all"):
    """Sets up a server, archives, distributes and runs Gunicorn instance of
    a folder on the available servers.

    Args:
        folder (str): The name of the folder to pack and upload.
    """
    print("Setting up web server... ")
    setup_webserver()
    print("Web server setup completed!")

    if folder == "all":
        for f in ["models", "api", "web_flask"]:
            print(f"Uploading {f}... ")
            pack_and_upload(f)
    else:
        pack_and_upload(folder)

    start_apps()
