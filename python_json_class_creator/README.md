# Python-Json-Class-Creator

I spent a lot of time creating Python classes for Json data I got interaction with all kinds of APIs so I wrote a script to turn Json data into properly typehinted Python classes.

```py
JSON_DATA: list[dict[str, typing.Any]] = ...
# A list of data of the SAME FORMAT you get in any way, like API calls.

from create import create
create(name='SomeClass', data=JSON_DATA)
```
That's it! The classes get saved to `classes.py` which can be used like:
```py
from classes import SomeClass

JSON_DATA: list[dict[str, typing.Any]] = ...
instances = [SomeClass(**data) for data in JSON_DATA]

"""Example use case where JSON_DATA looks something like
[
  {"arg": 123, ...},
  {"arg": 456, ...},
  ...
]
"""
for ins in instances:
  if ins.arg == 123:
    do_useful_things(ins=ins)
```
The more data you supply, the more accurate it will be.
The algorithm is not very efficient, but as you only really require to run this once, it is no problem.

For a good example:
Check `example.py` where it turns `example.json` into `classes.py` for a use case like `usage.py`.
