# The PV Secrets Vault

Copyright &copy; 2025 @ctx400.

Licensed for use under the terms of the [MIT license](LICENSE.md).
(https://opensource.org/license/mit)

A simple, secure vault for storing arbitrary secrets, serializable to
JSON, and easy to integrate into other projects.

# API Overview

PV's API is meant to be easy to use, and easy to integrate into other
projects. Below are some examples of normal usage.

## Basic Usage Recipies

```py
# Create a new vault
pv = PV()
pv.save('pv.json')

# Load an existing vault
pv = PV.load('pv.json')

# Create new secrets
pv.store_secret('mykey', 'mysecret', b'master_password')
pv.store_secret('google', 'mygooglepassword123', b'master_password')
pv.save('pv.json')

# List all secrets
print(pv.list_secrets())

# Read a secret
print(pv.read_secret('mykey', b'master_password'))

# Delete a secret
pv.delete_secret('mykey')
```

# Command-Line Tool

PV Provides a basic command-line application implementation of
the secrets vault. The module is a thin wrapper over PV's API.

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
