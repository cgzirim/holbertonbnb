# HolbertonBnB - Automatic Deployment Script :rocket:

Fabric script to automate remote deployment of HolbertonBnB.

## Dependencies :couple:

| Tool/Library | Version |
| ------------ | ------- |
| Python       | ^3.7.3  |
| gunicorn     | ^19.9.0 |
| Fabric       | ^2.4.0  |

## Usage :bicyclist:

[fabfile.py](): Fabric fabfile to deploy HolbertonBnB to given web servers.
- Run `fab --list` to see available commands.
- Usage: `fab <script>:<argument> --<option>=<value>`
- Options:
  - `deploy_loadbalancer`: Configures an Ubuntu machine to distribute traffic to specified web servers.
  - `pack --folder=STR`: Creates a tar archive.
  - `upload --archive=STR`: Distributes a tar archive.
  - `pack-and-upload --folder=STR`: Creates and distributes a tar archive.
  - `setup_webserver`: Prepares an Ubuntu machine to serve HolbertonBnB apps.
  - `start_apps`: Starts the WSGI apps.
  - `deploy_webservers` --folder=STR: All of the above for a given folder(s).

## Author :black_nib:
* __Chigozirim Igweamaka__ - <[chigozirim](https://github.com/iChigozirim)>
