import os
import pwd
import shutil
import socket
import sys
import tempfile

from subprocess import Popen, PIPE
from flask import Flask, request, make_response

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

    # Add in optional args from request parameters
    optional_flags = [
        "prefer-source",
        "prefer-dist",
        "prefer-stable",
        "dev",
        "no-dev",
        "with-dependencies",
        "force-error"
    ]
    for option in optional_flags:
        try:
            if option in request.form:
                args.append('--{}'.format(option))
        except:
            pass

    # Prepare to switch to 'nobody' so that we do not run
    # composer as 'root'
    pw_record = pwd.getpwnam('nobody')
    user_name = pw_record.pw_name
    user_home_dir = pw_record.pw_dir
    user_uid = pw_record.pw_uid
    user_gid = pw_record.pw_gid
    env = os.environ.copy()
    env['HOME'] = workdir # Use user_home_dir if not 'nobody'
    env['LOGNAME'] = user_name
    env['PWD'] = workdir
    env['USER'] = user_name

    # Make our working directory usable by 'nobody' user
    os.chown(workdir, user_uid, user_gid)

    # Get the required composer.json file
    f = request.files['composer-json']
    f.save(composerjson)
    os.chown(composerjson, user_uid, user_gid)
    # Get the optional composer.lock file, if provided
    if 'composer-lock' in request.files:
        f = request.files['composer-lock']
        f.save(composerlock)
        os.chown(composerlock, user_uid, user_gid)

    # Log what we are about to do
    print >> sys.stderr, 'Run composer as {}:'.format(user_name)
    print >> sys.stderr, args

    # Run composer as 'nobody'
    p = Popen(
        args,
        stdout=PIPE,
        stderr=PIPE,
        preexec_fn=demote(user_uid, user_gid),
        cwd=workdir,
        env=env
    )
    stdout, stderr = p.communicate()

    status = 200
    if p.returncode:
        # If the composer command failed, return an error status code
        # and write Composer's stder as the page output
        result = stderr
        # TODO: what is the best status code for failed updates?
        status = 400
    else:
        # If the composer command succeeded, read and print the resulting
        # composer.lock file
        fp = open(composerlock, "r")
        result = fp.read()

    # Clean up working directory once we're done
    shutil.rmtree(workdir)

    resp = make_response(result, status)
    resp.headers['Content-Type'] = 'text/plain'
    return resp

# From https://stackoverflow.com/questions/1770209/run-child-processes-as-different-user-from-a-long-running-process/6037494#6037494
def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result
