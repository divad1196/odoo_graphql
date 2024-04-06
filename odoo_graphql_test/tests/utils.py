import json
from pathlib import Path


def pretty_print(data, indent=4):
    print(json.dumps(data, indent=indent))


def _current_file_path():
    return Path(__file__).absolute().parent / "queries"


def open_query(file, *args, **kw):
    file = (_current_file_path() / file).resolve()
    return open(file, *args, **kw)


def get_query(file, *args, **kw):
    with open_query(file, *args, **kw) as f:
        query = f.read()
    return query


def contains(data, fields):
    return all(f in data for f in fields)


def firstMatching(data, predicat):
    for x in data:
        if predicat(x):
            return x
    return None
