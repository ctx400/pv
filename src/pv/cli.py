'''# The PV CLI

Provides a basic command-line application implementation of
the PV secrets vault. The module is a thin wrapper over PV's API.

## Basic Usage Recipies

Create a new vault:

```console
user@host:~$ pv create --path pv.json
Master Password: ********
Confirm Password: ********

user@host:~$
```

Store a secret in the vault:

> **Tip:** As a shortcut, you can set the `PV_PATH` environment variable
  to avoid having to pass `--path` to every command. If you're brave
  enough, you can also set `PV_PASSWORD` to avoid typing your master
  password for every `store` and `read` operation.

```console
user@host:~$ export PV_PATH='pv.json'
user@host:~$ export PV_PASSWORD='my master password'
user@host:~$ pv store mykey
Secret Value: ********

user@host:~$
```

List all secrets in a vault:

```console
user@host:~$ pv list
secret1
hello-world
google
dunkin
some-api-key

user@host:~$
```

Read a secret from the vault:

```console
user@host:~$ pv read mykey
my secret value

user@host:~$
```

Delete a secret from the vault:

```console
user@host:~$ pv delete mykey
user@host:~$
```

To get help on any command, just run:

```console
user@host:~$ pv COMMAND --help
user@host:~$
```
'''

# stdlib imports
import os as _os
from getpass import getpass as _getpass
from pathlib import Path as _Path
from typing import Optional as _Optional

# 3rd-party imports
import click as _click

# library imports
from pv import PV, Argon2idKDF

#
# Export Control
#
__all__ = []

#
# kwargs for various arguments
#
common_args = { #type:ignore
    'path_type': _Path,
    'allow_dash': False,
    'dir_okay': False,
    'file_okay': True,
    'executable': False,
    'resolve_path': True,
}
write_args = { #type:ignore
    **common_args,
    'exists': False,
    'writable': True,
    'readable': False,
}
readwrite_args = { #type:ignore
    **common_args,
    'exists': True,
    'writable': True,
    'readable': True,
}
read_args = { #type:ignore
    **common_args,
    'exists': True,
    'writable': False,
    'readable': True,
}


#
# Capture the master password from an environment variable, if set.
#
MASTER_PASSWORD: _Optional[str] = _os.environ.get('PV_PASSWORD')


# Dummy function as the root command
@_click.group()
@_click.version_option(
    package_name='pv',
    prog_name='The PV Secrets Vault',
    message='''\
%(prog)s, version %(version)s
Copyright (c) 2025 ctx400 (https://github.com/ctx400).

Licensed for use under the terms of the MIT license.
(https://github.com/ctx400/pv/blob/main/LICENSE.md)
''')
def pv() -> None:
    '''# The PV Secrets Vault CLI

    A secure vault for storing arbitrary secrets.

    ## Help

    To view help for a command, run `pv COMMAND --help`.

    ## Environment Variables

    Certain options, such as --path or the master key, can be provided
    via environment variables. The following environment variables can
    be set:

    \b
    | Variable    | Description                |
    | ----------- | -------------------------- |
    | PV_PATH     | Path to a PV vault.        |
    | PV_PASSWORD | A vault's master password. |
    '''


# Create a new PV vault.
@pv.command('create')
@_click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=_click.Path(**write_args)) #type:ignore
@_click.option('--memory-cost',
              type=_click.INT,
              required=False,
              default=None,
              help='Argon2id Memory Cost (dangerous option!)')
@_click.option('--iterations',
              type=_click.INT,
              required=False,
              default=None,
              help='Argon2id Iterations (dangerous option!)')
@_click.option('--parallelism',
              type=_click.INT,
              required=False,
              default=None,
              help='Argon2id Parallelism (dangerous option!)')
def create_vault(path: _Path,
                 memory_cost: _Optional[int],
                 iterations: _Optional[int],
                 parallelism: _Optional[int]) -> None:
    '''Create a new, empty vault.

    USAGE: `pv create --path pv.json`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    master_password: str = MASTER_PASSWORD or _getpass('Master Password: ')
    confirm_password: str = MASTER_PASSWORD or _getpass('Confirm Password: ')
    if master_password != confirm_password:
        print('ERROR: passwords do not match.')
        return

    argon2id_params: dict[str, int] = {}
    if memory_cost:
        argon2id_params['memory_cost'] = memory_cost
    if iterations:
        argon2id_params['iterations'] = iterations
    if parallelism:
        argon2id_params['parallelism'] = parallelism

    argon2id = Argon2idKDF(**argon2id_params)
    pv = PV.init(master_password, argon2id)
    pv.save(path)


# Store a secret in the vault.
@pv.command('store')
@_click.argument(
        'key',
        required=True,
        type=_click.STRING)
@_click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=_click.Path(**readwrite_args)) #type:ignore
@_click.option(
        '--unsafe-value', 'value',
        required=False,
        default=None,
        help='Unsafely set the value directly on the cli.',
        type=_click.STRING)
def store_secret(key: str, path: _Path, value: _Optional[str]) -> None:
    '''Store a secret in the vault.

    USAGE: `pv store --path pv.json KEY`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    secret: str = value or _getpass('Secret Value: ')
    password: str = MASTER_PASSWORD or _getpass('Master Password: ')
    pv = PV.load(path)
    pv.store_secret(key, secret, password)
    pv.save(path)


# Read a secret from the vault.
@pv.command('read')
@_click.argument(
        'key',
        required=True,
        type=_click.STRING)
@_click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=_click.Path(**read_args)) #type:ignore
def read_secret(key: str, path: _Path) -> None:
    '''Read a secret from the vault.

    USAGE: `pv read --path pv.json KEY`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    password: str = MASTER_PASSWORD or _getpass('Master Password: ')
    pv = PV.load(path)
    print(pv.read_secret(key, password))


# Delete a secret from the vault.
@pv.command('delete')
@_click.argument(
        'key',
        required=True,
        type=_click.STRING)
@_click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=_click.Path(**readwrite_args)) #type:ignore
def delete_secret(key: str, path: _Path) -> None:
    '''Delete a secret from the vault.

    USAGE: `pv delete --path pv.json KEY`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    pv = PV.load(path)
    pv.delete_secret(key)
    pv.save(path)


# List all secrets in the vault.
@pv.command('list')
@_click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=_click.Path(**read_args)) #type:ignore
def list_secrets(path: _Path) -> None:
    '''List all secrets in the vault.

    USAGE: `pv list --path pv.json`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    pv = PV.load(path)
    [print(key) for key in pv.list_secrets()]
