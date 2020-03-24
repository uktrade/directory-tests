# -*- coding: utf-8 -*-
"""Env var writer
Creates .env_* files in two forms:
1) with `export ` prefix (.env_with_export), for `source ` or `. ` shell commands
2) without `export ` prefix (.env_without_export), for docker-compose from prefixed host env vars

Example config:
    {
      "file_path": ".env-postgres",
      "env_vars": {
        "required": [
          "POSTGRES_DB",
          "POSTGRES_USER",
          "POSTGRES_PASSWORD"
        ],
        "optional": []
      }
    }

Usage:
  env_writer.py (--env=dev | --env=stage | --env=prod) [--config=ENV_FILE]
  env_writer.py (-h | --help)
  env_writer.py --version

Options:
  -h --help             Show this screen.
  --config=ENV_FILE     Specify input config file [default: ./env_vars/env.json]
  --env=ENV             Use environment variables prefixed with "ENV_"
  --version             Show version.
"""
import json
import os
import sys

from docopt import docopt


class DockerComposeEnvWriter:
    @staticmethod
    def save_env_vars(
        configuration: dict, all_env_vars: dict, env_prefix: str, export_mode: bool
    ):
        if export_mode:
            filename = "{}_with_export".format(configuration["file_path"])
        else:
            filename = "{}_without_export".format(configuration["file_path"])
        with open(filename, "w") as destination:
            for var in all_env_vars:
                # Get value of the prefixed host env var
                value = os.getenv(f"{env_prefix}_{var}")
                if value:
                    special_chars = "!$"
                    if export_mode:
                        if any(special in value for special in special_chars):
                            destination.write("export {}='{}'\n".format(var, value))
                        else:
                            destination.write("export {}={}\n".format(var, value))
                    else:
                        destination.write("{}={}\n".format(var, value))

    @classmethod
    def create(cls, configuration: dict, env_prefix: str):
        cls.validate(configuration, env_prefix)

        all_env_vars = (
            configuration["env_vars"]["required"]
            + configuration["env_vars"]["optional"]
        )
        cls.save_env_vars(configuration, all_env_vars, env_prefix, export_mode=True)
        cls.save_env_vars(configuration, all_env_vars, env_prefix, export_mode=False)

    @staticmethod
    def validate(config: dict, env_prefix: str):
        unset_required_host_vars = [
            var
            for var in config["env_vars"]["required"]
            if not os.getenv(f"{env_prefix}_{var}")
        ]

        if unset_required_host_vars:
            sys.exit(
                "Required host environment variables are not set: \n{}".format(
                    "\n".join(unset_required_host_vars)
                )
            )


if __name__ == "__main__":
    arguments = docopt(__doc__, version="env_writer 1.0")
    path_to_config = arguments["--config"]
    env_prefix = arguments["--env"].upper()
    with open(path_to_config, "r") as src:
        config = json.load(src)

    DockerComposeEnvWriter.create(config, env_prefix)
