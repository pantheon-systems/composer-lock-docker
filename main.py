import os
import socket

from flask import Flask

app = Flask(__name__)

@app.route('/')
def composer_lock_info():
    hostname = socket.gethostname()
    return 'Composer lock service running on {}\n'.format(hostname)

