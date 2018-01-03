docker composer-lock service (flask app)
========================================

Provides a "composer lock" service as a Python Flask app in a docker container.

To use the service, upload a `composer.json` file to a specified endpoint
uri. The result will be the updated contents of the `composer.lock` file.

Supported endpoints:

- `/update`: Runs a `composer update` on the provided `composer.json` file.
- `/update&project=org/name:^1`: Runs `composer update` on the specified project(s) only.

Upload files:

- Upload `composer-json` to supply the composer.json file (required).
- Upload `composer-lock` to supply an initial lock file (optional).

Additional flags to pass via curl:

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

Build & Push
-------------

- Run `make build` for local testing.

This project has been registered on quay.io; push to the master branch to
automatically update :latest for the container.

Run local
---------

Start container:

```
$ docker run --rm -p 5000:5000 quay.io/getpantheon/composer-lock
 * Serving Flask app "main"
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Curl it:

```
$ curl localhost:5000/update
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

Note: If you're on OSX, you need to run `docker-machine ip default` (assuming
`default` is the name of your docker-machine instance) in order to get the IP
of the docker VM instead of using `localhost`, example:

```
$ docker-machine ip default
192.168.99.100

$ curl 192.168.99.100:5000/update
...

## or:

$ curl $(docker-machine ip default):5000/update
...
```

Run on Kubernetes
-----------------
See `examples/kubernetes` directory for files. Customize to suit, then run:

```
$ cd examples/kubernetes
$ kubectl apply -f deploy.yaml
$ kubectl apply -f service.yaml
```
