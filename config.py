import os

from dynaconf import Dynaconf

root_path = os.path.dirname(os.path.realpath(__file__))

settings = Dynaconf(
    root_path=root_path,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=["default"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
