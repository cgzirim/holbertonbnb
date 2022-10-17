#!/usr/bin/python3
"""Handles interactions with HBNB console remote connections."""
import os
import pty
import fcntl
import struct
import select
import termios
import subprocess
from os import environ
from signal import SIGKILL
from flask import Flask, request
from flask_socketio import SocketIO


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(
    app, ping_timeout=60,
    ping_interval=5,
    cors_allowed_origins="*")

clients = {}


def set_winsize(fd, row, col, xpix=0, ypix=0):
    """Sets window size with termios."""
    winsize = struct.pack("HHHH", row, col, xpix, ypix)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


def read_and_forward_console_output(fd, client_id, child_pid):
    """Reads the output from the console program in the child process and
    forward it to the remote console.
    """
    max_read_bytes = 1024 * 20
    while True:
        socketio.sleep(0.01)
        if fd:
            timeout_sec = 0
            (data_ready, _, _) = select.select([fd], [], [], timeout_sec)
            if data_ready:
                try:
                    # check if the child process for the remote console is dead
                    os.kill(child_pid, 0)

                    output = os.read(fd, max_read_bytes).decode(errors="ignore")
                    socketio.emit(
                        "console-output", {"output": output}, to=client_id)

                    exit_msg = "Well, that sure was fun!"
                    if exit_msg in output:
                        socketio.emit("end", to=client_id)

                except OSError:
                    # ends the client's connection if the child pid has been
                    # killed
                    socketio.emit("end", to=client_id)
                    return


@socketio.on("console-input")
def console_input(data):
    """Take input from the remote console and write it to the child pty."""
    client = clients[request.sid]
    fd = client.get("fd")
    if fd:
        # watch out for SIGINT; disconnect the client upon receiving ctrl+C
        ascii_values = [ord(char) for char in data["input"]]
        if ascii_values and ascii_values[0] == 3:
            socketio.emit("end", to=request.sid)

        os.write(fd, data["input"].encode())
        read_and_forward_console_output(fd, request.sid, client["child_pid"])


@socketio.on("resize")
def resize(data):
    fd = clients[request.sid].get("fd")
    if fd:
        set_winsize(fd, data["rows"], data["cols"])


@socketio.on("connect")
def connect():
    """New client connected.
    Create a child process running the hbnb console program which the client
    would read from and write to.
    """
    path_to_console = environ.get("HBNB_CONSOLE_PATH") or "/data/console.py"
    (child_pid, fd) = pty.fork()
    if child_pid == 0:
        subprocess.run(path_to_console)
    else:
        # This is the parent process fork.
        # store child fd and pid
        clients[request.sid] = {"fd": fd, "child_pid": child_pid}
        set_winsize(fd, 50, 50)


@socketio.on("disconnect")
def disconnect():
    """Remove client from dict of connected clients, kill the child pid
    if it's still running.
    """
    client = clients[request.sid]

    try:
        os.kill(client["child_pid"], 0)
    except OSError:
        # Do nothing if the child pid doesn't exist
        pass
    else:
        os.kill(client["child_pid"], SIGKILL)
    del clients[request.sid]


if __name__ == "__main__":
    """Main function."""
    socketio.run(
        app,
        debug=False,
        port=5005,
        host="0.0.0.0",
        keyfile="privkey.pem",
        certfile="fullchain.pem",
    )
