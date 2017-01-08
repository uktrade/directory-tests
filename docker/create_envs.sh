#!/bin/bash -xe

python ./docker/env_writer.py \
    ./docker/env.json \
    ./docker/env-postgres.json \
    ./docker/directory-api/env.json \
    ./docker/directory-sso-proxy/env.json \
    ./docker/directory-sso/env.json \
    ./docker/directory-ui-buyer/env.json \
    ./docker/directory-ui-supplier/env.json
