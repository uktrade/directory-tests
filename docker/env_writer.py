"""Env var writer
Creates .env_* files in two forms:
1) with `export ` prefix (.env_with_export), for `source ` or `. ` shell commands
2) without `export ` prefix (.env_without_export), for docker-compose from prefixed host env vars

Example config:
    {
      "host_env_var_prefix": "DIRECTORY",
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
  --config=ENV_FILE     Specify input config file [default: ./docker/env.json]
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
            config: dict, all_env_vars: dict, env_prefix: str,
            export_mode: bool
    ):
        if export_mode:
            filename = "{}_with_export".format(config["file_path"])
        else:
            filename = "{}_without_export".format(config["file_path"])
        with open(filename, "w") as dest:
            for var in all_env_vars:
                # Get value of the prefixed host env var
                value = os.getenv(
                    f"{env_prefix}_{config['host_env_var_prefix']}_{var}"
                )
                if value:
                    special_chars = "!$"
                    if export_mode:
                        if any(special in value for special in special_chars):
                            dest.write("export {}='{}'\n".format(var, value))
                        else:
                            dest.write("export {}={}\n".format(var, value))
                    else:
                        dest.write("{}={}\n".format(var, value))

    @classmethod
    def create(cls, config: dict, env_prefix: str):
        cls.validate(config, env_prefix)

        all_env_vars = (
            config["env_vars"]["required"] + config["env_vars"]["optional"]
        )
        cls.save_env_vars(config, all_env_vars, env_prefix, export_mode=True)
        cls.save_env_vars(config, all_env_vars, env_prefix, export_mode=False)

    @staticmethod
    def validate(config: dict, env_prefix: str):
        unset_required_host_vars = [
            var
            for var in config["env_vars"]["required"]
            if not os.getenv(
                f"{env_prefix}_{config['host_env_var_prefix']}_{var}"
            )
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
    with open(path_to_config, 'r') as src:
        config = json.load(src)

    DockerComposeEnvWriter.create(config, env_prefix)
