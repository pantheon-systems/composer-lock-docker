import os
import shutil
import socket
import tempfile

from subprocess import call

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def composer_lock_service_info():
    hostname = socket.gethostname()
    return '# Composer lock service running on {}\n'.format(hostname)

@app.route('/update', methods=['POST'])
def composer_lock_update():
    # Create a temporary working directory
    workdir = tempfile.mkdtemp()
    composerjson = os.path.join(workdir, 'composer.json')
    composerlock = os.path.join(workdir, 'composer.lock')

    # Get the required composer.json file
    f = request.files['composer-json']
    f.save(composerjson)
    # Get the optional composer.lock file, if provided
    if 'composer-lock' in request.files:
        f = request.files['composer-lock']
        f.save(composerlock)

    # Mandatory arguments for Composer
    args = [
        "composer",
        "update",
        '--working-dir={}'.format(workdir),
        "--no-autoloader",
        "--no-scripts",
        "--no-interaction",
        "--no-plugins",
        "--profile"
    ]

    # TODO: Add in optional args from request parameters

    # Run composer
    call(args)

    # Read and print the resulting composer.lock file
    fp = open(composerlock, "r")
    result = fp.read()

    # Clean up working directory once we're done
    shutil.rmtree(workdir)

    return result
