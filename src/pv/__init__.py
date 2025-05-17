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


@click.group()
def pv() -> None:
    pass

@pv.command('create')
@click.argument('path',
                required=True,
                type=click.Path(
                    path_type=Path,
                    allow_dash=False,
                    exists=False,
                    dir_okay=False,
                    file_okay=True,
                    resolve_path=True,
                    writable=True,
                    readable=False,
                    executable=False,
                ))
def create_vault(path: Path) -> None:
    pv = PV()
    pv.save(path)

@pv.command('store')
@click.argument('key',
                required=True,
                type=click.STRING)
@click.argument('path',
                required=True,
                type=click.Path(
                    path_type=Path,
                    allow_dash=False,
                    exists=True,
                    dir_okay=False,
                    file_okay=True,
                    resolve_path=True,
                    writable=True,
                    readable=True,
                    executable=False,
                ))
def store_secret(key: str, path: Path) -> None:
    secret: str = getpass('Secret Value: ')
    password: bytes = getpass('Master Password: ').encode()
    pv = PV.load(path)
    pv.store_secret(key, secret, password)
    pv.save(path)

@pv.command('read')
@click.argument('key',
                required=True,
                type=click.STRING)
@click.argument('path',
                required=True,
                type=click.Path(
                    path_type=Path,
                    allow_dash=False,
                    exists=True,
                    dir_okay=False,
                    file_okay=True,
                    resolve_path=True,
                    writable=False,
                    readable=True,
                    executable=False,
                ))
def read_secret(key: str, path: Path) -> None:
    password: bytes = getpass('Master Password: ').encode()
    pv = PV.load(path)
    print(pv.read_secret(key, password))

@pv.command('delete')
@click.argument('key',
                required=True,
                type=click.STRING)
@click.argument('path',
                required=True,
                type=click.Path(
                    path_type=Path,
                    allow_dash=False,
                    exists=True,
                    dir_okay=False,
                    file_okay=True,
                    resolve_path=True,
                    writable=True,
                    readable=True,
                    executable=False,
                ))
def delete_secret(key: str, path: Path) -> None:
    pv = PV.load(path)
    pv.delete_secret(key)
    pv.save(path)

@pv.command('list')
@click.argument('path',
                required=True,
                type=click.Path(
                    path_type=Path,
                    allow_dash=False,
                    exists=True,
                    dir_okay=False,
                    file_okay=True,
                    resolve_path=True,
                    writable=False,
                    readable=True,
                    executable=False,
                ))
def list_secrets(path: Path) -> None:
    pv = PV.load(path)
    [print(key) for key in pv.list_secrets()]
