# The PV Secrets Vault

Copyright &copy; 2025 @ctx400.

Licensed for use under the terms of the [MIT license](LICENSE.md).
(https://opensource.org/license/mit)

A simple, secure vault for storing arbitrary secrets, serializable to
JSON, and easy to integrate into other projects.

## Contents

- [Installation](#installation)
- [API Overview](#api-overview)
- [Command-Line Tool](#command-line-tool)

## Installation

Option 1: Install with `pip`:

```sh
pip install git+https://github.com/ctx400/pv@2.1.0
pv --version
```

Option 2: Install with `pip` in a virtual environment:

```sh
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/ctx400/pv@2.1.0
pv --version
```

Option 3: Install the CLI with `uv`:

```sh
uv tool install git+https://github.com/ctx400/pv@2.1.0
pv --version
```

Option 4: Add to a `uv`-managed Python project:

```sh
uv init myproject
cd myproject/
uv add git+https://github.com/ctx400/pv@2.1.0
pv --version
```

## API Overview

PV's API is meant to be easy to use, and easy to integrate into other
projects. Below are some examples of normal usage.

Full API docs [here](https://ctx400.github.io/pv)

### Basic Usage Recipies

```py
from pv import PV

# Create a new vault
pv = PV.init('master_password')
pv.save('pv.json')

# Load an existing vault
pv = PV.load('pv.json')

# Create new secrets
pv.store_secret('mykey', 'mysecret', 'master_password')
pv.store_secret('google', 'mygooglepassword123', 'master_password')
pv.save('pv.json')

# List all secrets
print(pv.list_secrets())

# Read a secret
print(pv.read_secret('mykey', 'master_password'))

# Delete a secret
pv.delete_secret('mykey')
```

## Command-Line Tool

PV Provides a basic command-line application implementation of
the secrets vault. The module is a thin wrapper over PV's API.

### Basic Usage Recipies

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
user@host:~$ export PV_PASSWORD='my-master-password'
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
