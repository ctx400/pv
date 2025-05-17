# stdlib imports
from getpass import getpass
from pathlib import Path

# 3rd-party imports
import click

# re-exports
from .vault import PV as PV
from .vault import Secret as Secret
from .vault import Argon2idKDF as Argon2idKDF
from .vault import new_salt as new_salt


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
create_args = { #type:ignore
    **common_args,
    'exists': False,
    'writable': True,
    'readable': False,
}
store_args = { #type:ignore
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
        type=click.Path(**create_args)) #type:ignore
def create_vault(path: Path) -> None:
    pv = PV()
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
        type=click.Path(**store_args)) #type:ignore
def store_secret(key: str, path: Path) -> None:
    secret: str = getpass('Secret Value: ')
    password: bytes = getpass('Master Password: ').encode()
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
    password: bytes = getpass('Master Password: ').encode()
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
        type=click.Path(**store_args)) #type:ignore
def delete_secret(key: str, path: Path) -> None:
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
    pv = PV.load(path)
    [print(key) for key in pv.list_secrets()]
