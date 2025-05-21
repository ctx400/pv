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
from getpass import getpass
from pathlib import Path

# 3rd-party imports
import click

# library imports
from pv import PV


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


# Dummy function as the root command
@click.group()
def pv() -> None:
    pass


# Create a new PV vault.
@pv.command('create')
@click.argument(
        'path',
        required=True,
        type=click.Path(**write_args)) #type:ignore
def create_vault(path: Path) -> None:
    '''Create a new, empty vault.

    USAGE: `pv create PATH.json`
    '''

    master_password: str = getpass('Master Password: ')
    confirm_password: str = getpass('Confirm Password: ')
    if master_password != confirm_password:
        print('ERROR: passwords do not match.')
        return
    pv = PV.init(master_password)
    pv.save(path)


# Store a secret in the vault.
@pv.command('store')
@click.argument(
        'key',
        required=True,
        type=click.STRING)
@click.argument(
        'path',
        required=True,
        type=click.Path(**readwrite_args)) #type:ignore
def store_secret(key: str, path: Path) -> None:
    '''Store a secret in the vault.

    USAGE: `pv store KEY PATH.json`
    '''

    secret: str = getpass('Secret Value: ')
    password: str = getpass('Master Password: ')
    pv = PV.load(path)
    pv.store_secret(key, secret, password)
    pv.save(path)


# Read a secret from the vault.
@pv.command('read')
@click.argument(
        'key',
        required=True,
        type=click.STRING)
@click.argument(
        'path',
        required=True,
        type=click.Path(**read_args)) #type:ignore
def read_secret(key: str, path: Path) -> None:
    '''Read a secret from the vault.

    USAGE: `pv read KEY PATH.json`
    '''

    password: str = getpass('Master Password: ')
    pv = PV.load(path)
    print(pv.read_secret(key, password))


# Delete a secret from the vault.
@pv.command('delete')
@click.argument(
        'key',
        required=True,
        type=click.STRING)
@click.argument(
        'path',
        required=True,
        type=click.Path(**readwrite_args)) #type:ignore
def delete_secret(key: str, path: Path) -> None:
    '''Delete a secret from the vault.

    USAGE: `pv delete KEY PATH.json`
    '''

    pv = PV.load(path)
    pv.delete_secret(key)
    pv.save(path)


# List all secrets in the vault.
@pv.command('list')
@click.argument(
        'path',
        required=True,
        type=click.Path(**read_args)) #type:ignore
def list_secrets(path: Path) -> None:
    '''List all secrets in the vault.

    USAGE: `pv list PATH.json`
    '''

    pv = PV.load(path)
    [print(key) for key in pv.list_secrets()]
