# STRINGX

**STRINGX** is a [STRING](https://string-db.org) API client using [HTTPX](https://www.python-httpx.org).

## Quickstart

```sh
pip install stringx
```

```python
import stringx
```

Firstly, it is recommended that you disambiguate your list of identifiers.

```python
identifiers = ["edin", "atta"]

disambiguated_identifiers = stringx.map_identifiers(identifiers, species=7227)
```

The `disambiguated_identifiers` JSON response can be manipulated and reused in follow-up calls. For instance:

```python
stringx.network(identifiers, species=7227)
stringx.interaction_partners(identifiers, species=7227)
```

## Documentation

Here are some important point to have in mind when using `stringx`:

- Latest API version tested and targeted by default.
- You should identify yourself beforehand.
- `POST` requests whenever possible as recommended.
- _Currently_, only `json` format supported.
- When applicable, `species` field is mandatory.
- Use a custom `stringx.Client()` if you plan to make multiple calls or need to target a previous API version.

```python
import stringx

with stringx.Client(base_url="https://version-11-0.string-db.org") as db:
    # remember to disambiguate identifiers first if needed
    network_1 = db.network(identifiers_1, species=7227)
    network_2 = db.network(identifiers_2, species=9606)
```

This tool aims at following best practices defined by STRING.
Refer to the official [API documentation](https://string-db.org/help/api) for details.

## API Endpoints Implemented

| Method                              | API URL                         | **stringx**              |
| ----------------------------------- | ------------------------------- | ------------------------ |
| Mapping identifiers                 | /api/json/get_string_ids?       | `map_identifiers()`      |
| Retrieving the interaction network  | /api/tsv/network?               | `network()`              |
| Retrieving the interaction partners | /api/json/interaction_partners? | `interaction_partners()` |
