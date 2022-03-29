docker composer-lock service (flask app)
========================================

[![Deprecated](https://img.shields.io/badge/Pantheon-Deprecated-yellow?logo=pantheon&color=FFDC28)](https://pantheon.io/docs/oss-support-levels#deprecated)

Provides a "composer lock" service as a Python Flask app in a docker container.

To use the service, upload a `composer.json` file to a specified endpoint
uri. The result will be the updated contents of the `composer.lock` file.

Supported endpoints:

- `/update`: Runs a `composer update` on the provided `composer.json` file.
- `/update&project=org/name`: Runs `composer update` on the specified project(s) only.

Upload files:

- Upload `composer-json` to supply the composer.json file (required).
- Upload `composer-lock` to supply an initial lock file (optional).

Additional flags may be provided via curl:

- `prefer-source`
- `prefer-dist`
- `prefer-stable`
- `dev`
- `no-dev`
- `with-dependencies`

The following options are assumed:

- `--no-autoloader`
- `--no-scripts`
- `--no-interaction`
- `--no-plugins`

No other `composer` options may be set when using this service.

Build & Push
-------------

- Run `make build` for local testing.

This project has been registered on quay.io; push to the master branch to
automatically update :latest for the container.

Run local
---------

Start container:

```
$ docker run --rm -p 5000:5000 quay.io/pantheon-public/composer-lock
 * Serving Flask app "main"
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Curl it:

```
$ curl localhost:5000
# Composer lock service running on 85d3082ca94f
```

If you want to know the exact IP address of the local docker image, you
can use:

`docker-machine ip default` 

(assuming `default` is the name of your docker-machine instance)

Use this if `localhost` does not work for local testing.

Run on Kubernetes
-----------------
See `examples/kubernetes` directory for files. Customize to suit (optional), 
then run:

```
$ cd examples/kubernetes
$ kubectl apply -f deploy.yaml
$ kubectl apply -f service.yaml
$ kubectl get services composer-lock
```

Access the service via the address shown in the "External IP" column.

Example client usage
--------------------

```
$ export COMPOSER_LOCK_SERVICE = composer-lock.example.com
$ alias composer=/path/to/composer-lock-docker/examples/scripts/composer

$ composer update
```

Example service usage
---------------------

Upload a `composer.json` to get a `composer.lock` back:

```
$ curl -F 'composer-json=@/path/to/project/composer.json' localhost:5000/update
{
    "_readme": [
        "This file locks the dependencies of your project to a known state",
        "Read more about it at https://getcomposer.org/doc/01-basic-usage.md#composer-lock-the-lock-file",
        "This file is @generated automatically"
    ],
    "content-hash": "c755802dc01c48c0f80de1866ba616c5",
    "packages": [
        {
...
```

Pass the 'prefer-source' option:

```
$ curl -F 'composer-json=@composer.json' -F 'prefer-source=1' localhost:5000/update
...
```

TODO: Provide an existing lock file, and update just one project with its
dependencies:

```
$ curl \
  -F 'composer-json=@composer.json' \
  -F 'composer-lock=@composer.lock' \
  -F 'project=org/name' \
  -F 'with-dependencies=1' \
  localhost:5000/update
...
```

