#!/bin/bash -xe

python ./docker/env_writer.py \
    ./docker/env.json \
    ./docker/directory-api/env.json \
    ./docker/directory-api/env-postgres.json \
    ./docker/directory-sso/env.json \
    ./docker/directory-sso/env-postgres.json \
    ./docker/directory-ui/env.json
