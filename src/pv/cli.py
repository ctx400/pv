'''CLI implementation of PV.

Provides a basic command-line application implementation of
the PV secrets vault. The module is a thin wrapper over PV's API.

## Basic Usage Recipies

Create a new vault:

```console
user@host:~$ pv create pv.json
user@host:~$
```

Store a secret in the vault:

```console
user@host:~$ pv store mykey pv.json
Secret Value: ********
Master Password: ********

user@host:~$
```

List all secrets in a vault:

```console
user@host:~$ pv list pv.json
secret1
hello-world
google
dunkin
some-api-key

user@host:~$
```

Read a secret from the vault:

```console
user@host:~$ pv read mykey pv.json
Master Password: ********
my secret value

user@host:~$
```

Delete a secret from the vault:

```console
user@host:~$ pv delete mykey pv.json
user@host:~$
```
'''

# stdlib imports
import os
from getpass import getpass
from pathlib import Path
from typing import Optional

# 3rd-party imports
import click

# library imports
from pv import PV, Argon2idKDF


#
# kwargs for various arguments
#
common_args = { #type:ignore
    'path_type': Path,
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
MASTER_PASSWORD: Optional[str] = os.environ.get('PV_PASSWORD')


# Dummy function as the root command
@click.group()
@click.version_option(
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
@click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=click.Path(**write_args)) #type:ignore
@click.option('--memory-cost',
              type=click.INT,
              required=False,
              default=None,
              help='Argon2id Memory Cost (dangerous option!)')
@click.option('--iterations',
              type=click.INT,
              required=False,
              default=None,
              help='Argon2id Iterations (dangerous option!)')
@click.option('--parallelism',
              type=click.INT,
              required=False,
              default=None,
              help='Argon2id Parallelism (dangerous option!)')
def create_vault(path: Path,
                 memory_cost: Optional[int],
                 iterations: Optional[int],
                 parallelism: Optional[int]) -> None:
    '''Create a new, empty vault.

    USAGE: `pv create --path pv.json`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    master_password: str = MASTER_PASSWORD or getpass('Master Password: ')
    confirm_password: str = MASTER_PASSWORD or getpass('Confirm Password: ')
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
@click.argument(
        'key',
        required=True,
        type=click.STRING)
@click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=click.Path(**readwrite_args)) #type:ignore
def store_secret(key: str, path: Path) -> None:
    '''Store a secret in the vault.

    USAGE: `pv store --path pv.json KEY`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    secret: str = getpass('Secret Value: ')
    password: str = MASTER_PASSWORD or getpass('Master Password: ')
    pv = PV.load(path)
    pv.store_secret(key, secret, password)
    pv.save(path)


# Read a secret from the vault.
@pv.command('read')
@click.argument(
        'key',
        required=True,
        type=click.STRING)
@click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=click.Path(**read_args)) #type:ignore
def read_secret(key: str, path: Path) -> None:
    '''Read a secret from the vault.

    USAGE: `pv read --path pv.json KEY`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    password: str = MASTER_PASSWORD or getpass('Master Password: ')
    pv = PV.load(path)
    print(pv.read_secret(key, password))


# Delete a secret from the vault.
@pv.command('delete')
@click.argument(
        'key',
        required=True,
        type=click.STRING)
@click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=click.Path(**readwrite_args)) #type:ignore
def delete_secret(key: str, path: Path) -> None:
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
@click.option(
        '--path', '-p',
        envvar='PV_PATH',
        required=True,
        type=click.Path(**read_args)) #type:ignore
def list_secrets(path: Path) -> None:
    '''List all secrets in the vault.

    USAGE: `pv list --path pv.json`

    HINT: Instead of passing --path, you can also
    set the environment variable PV_PATH.
    '''

    pv = PV.load(path)
    [print(key) for key in pv.list_secrets()]
