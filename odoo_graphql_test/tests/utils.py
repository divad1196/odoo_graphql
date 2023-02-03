from pathlib import Path

def _current_file_path():
    return Path(__file__).absolute().parent / "queries"

def open_query(file, *args, **kw):
    file = (_current_file_path() / file).resolve()
    return open(file, *args, **kw)

def contains(data, fields):
    return all(f in data for f in fields)

def firstMatching(data, predicat):
    for x in data:
        if predicat(x):
            return x
    return None
