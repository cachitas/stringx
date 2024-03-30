# STRINGX

STRINGX is a [STRING](string-db.org) API client using [HTTPX](https://www.python-httpx.org)

## Install

```sh
pip install stringx
```

## Usage

```python
import stringx

with stringx.Client() as client:
    identifiers = client.map_identifiers(["edin", "atta"], species=7227)

```
