# STRINGX

[![PyPI Version](https://img.shields.io/pypi/v/stringx?label=PyPI&logo=pypi&logoColor=white&color=006dad)](https://pypi.org/project/stringx/)
[![Python Version](https://img.shields.io/pypi/pyversions/stringx?label=Python&logo=python&logoColor=white&color=006dad)](https://pypi.org/project/stringx/)
[![STRING Version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fstring-db.org%2Fapi%2Fjson%2Fversion&query=%24%5B0%5D.string_version&style=flat&label=STRING&color=f7f6f2)](https://string-db.org)

STRINGX is an API client for the [STRING] database, built on top of [HTTPX].

## Features

Inspired on the well-established usability of `httpx`, `stringx` provides a clean and easy to use interface to the STRING API while following usage recommendations and best practices:

- Requires client identification;
- Uses POST requests;
- Allows linking to a specific STRING version;
- When applicable, enforces specifying the `species` parameter.

A customizable client allows targeting any API version and provides support for all output formats available: TSV, JSON, XML, etc...

## Installation

STRINGX requires Python 3.9+ and is available on [PyPI](https://pypi.org/project/stringx).

```sh
$ pip install stringx
```

## Usage

The `stringx` module provides a direct interface to the current API version. JSON is the default response format and can be easily integrated with `pandas` for further processing.

```python
import pandas as pd
import stringx

stringx.identity = ""  # please identify yourself

df = pd.Dataframe(
    stringx.network(identifiers=["7227.FBpp0074940", "7227.FBpp0082908"], species=7227)
)
```

> [!TIP]
> STRING understands a variety of identifiers and does its best to disambiguate your input. Nevertheless, it is recommended to map your identifiers first. Querying the API with a disambiguated identifier (for example 9606.ENSP00000269305 for human TP53) will guarantee much faster server response.

## Client Identification

The STRING API requires its callers to identify themselves. To address this, STRINGX enforces that the `identity` value is set. If done at the module level all subsequent requests will carry this information.

```python
import stringx

stringx.identity = "my_project_name"
```

You can also identify your clients independently.

```python
import stringx

with stringx.Client(identity="my_project_name") as client:
    ...

with stringx.Client(
    address="https://version-10-5.string-db.org",
    identity="me@example.com"
) as client:
    ...
```

Regardless of how you choose to do it, STRINGX always appends its own information to your identity.

Using one of the clients instantiated above as example, the `caller_identity` parameters passed to the STRING API would be `my_project_name (python-stringx/x.y.z)`.

## Documentation

🚧🚧🚧

Refer to the official [API documentation](https://string-db.org/help/api) for details.

## License

[STRING] data is freely available under a [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) license. Please provide appropriate credit when using the data. No changes or additions are made to the data by STRINGX.

[STRING]: https://string-db.org
[HTTPX]: https://www.python-httpx.org
