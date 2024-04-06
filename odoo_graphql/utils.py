import json


# print node, used for debug
def print_node(node):
    print(json.dumps(node.to_dict(), indent=4))


def model2name(model):
    return "".join(p.title() for p in model.split("."))


# =======================================
# Helper to apply graphql nodes on python types
# This is mostly useful for introspection


class _Lazy:
    def __init__(self, func):
        self._func = func


def lazy(func):
    return _Lazy(func)


def _exec_lazy(obj):
    if isinstance(obj, _Lazy):
        return obj._func()
    return obj


def resolve_data(node, data):
    """
    The goal is to apply a graphql query on a python data, e.g. a dict
    It also lazily resolve data for performance if it founds a `lazy` data
    usage:

        def my_heavy_computation(): # No parameters, this is a closure
            ...

        resolve_data(node, {
            "name": "hello world",
            "data": lazy(my_heavy_computation),
        })
    """
    if not node or not isinstance(data, (dict, list, tuple)) or not node.selection_set:
        return data
    if isinstance(data, dict):
        result = {}
        for f in node.selection_set.selections:
            key = f.name.value
            value = resolve_data(f, _exec_lazy(data.get(key)))
            result[key] = value
        return result

    return [resolve_data(node, d) for d in data]
