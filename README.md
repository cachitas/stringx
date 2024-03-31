# STRINGX

STRINGX is a [STRING](https://string-db.org) API client using [HTTPX](https://www.python-httpx.org).

## Install

```sh
pip install stringx
```

## Usage

```python
import stringx
```

You can call API endpoints directly

```python
identifiers = stringx.map_identifiers(["edin", "atta"], species=7227)
```

or instantiate a customized client where you can specify the API version or your *caller identity*.


```python
import stringx

with stringx.Client(base_url="https://version-11-0.string-db.org") as client:
    identifiers = client.map_identifiers(["edin", "atta"], species=7227)

```

### API Endpoints

| Method                           | API URL                         | **stringx**              |
| -------------------------------- | ------------------------------- | ------------------------ |
| Mapping identifiers              | /api/json/get_string_ids?       | `map_identifiers()`      |
| Getting the interaction partners | /api/json/interaction_partners? | `interaction_partners()` |
