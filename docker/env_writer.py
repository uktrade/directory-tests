"""
Creates .env_* files in two forms:
1) with `export ` prefix (.env_with_export), for `source ` or `. ` shell commands
2) without `export ` prefix (.env_without_export), for docker-compose from prefixed host env vars

Usage: python docker-compose-env_writer.py <path_to_json_config>

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
"""
import json
import os
import sys


class DockerComposeEnvWriter:

    @staticmethod
    def save_env_vars(config, all_env_vars, export_mode):
        if export_mode:
            filename = '{}_with_export'.format(config['file_path'])
        else:
            filename = '{}_without_export'.format(config['file_path'])
        with open(filename, 'w') as dest:
            for var in all_env_vars:
                # Get value of the prefixed host env var
                value = os.getenv('{}_{}'.format(
                    config['host_env_var_prefix'],
                    var
                ))
                if value:
                    special_chars = '!$'
                    if export_mode:
                        if any(special in value for special in special_chars):
                            dest.write("export {}='{}'\n".format(var, value))
                        else:
                            dest.write("export {}={}\n".format(var, value))
                    else:
                        dest.write("{}={}\n".format(var, value))

    @classmethod
    def create(cls, config):
        cls.validate(config)

        all_env_vars = (
            config['env_vars']['required'] + config['env_vars']['optional']
        )
        cls.save_env_vars(config, all_env_vars, export_mode=True)
        cls.save_env_vars(config, all_env_vars, export_mode=False)

    @staticmethod
    def validate(config):
        unset_required_host_vars = [
            var for var in config['env_vars']['required']
            if not os.getenv('{}_{}'.format(
                config['host_env_var_prefix'], var
            ))
        ]

        if unset_required_host_vars:
            sys.exit(
                "Required host environment variables are not set: \n{}".format(
                    "\n".join(unset_required_host_vars)
                )
            )


if __name__ == '__main__':
    # TODO: change to docopt
    for path_to_config in sys.argv[1:]:
        with open(path_to_config, 'r') as src:
            config = json.load(src)

        DockerComposeEnvWriter.create(config)
