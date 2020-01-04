# **PRE-RELEASE SCAFFOLDING**
## **THIS PACKAGE IS NOT YET IMPLEMENTED**
## **Tentative release date: March 2020**

A port of the [Rimu Markup language](https://srackham.github.io/rimu/) written in the Python
language.


## Features
Functionally identical to the [JavaScript
implementation](https://github.com/srackham/rimu) version 11.1 with the
following exceptions:

- Does not support deprecated _Expression macro values_.
- Does not support deprecated _Imported Layouts_.


## Usage
Install from [PyPI](https://pypi.org/project/rimu/):

    pip install rimu

Example usage:

``` python
import rimu

def main():
  print(rimu.render('Hello *Rimu*!'))
```

See also Rimu
[API documentation](https://srackham.github.io/rimu/reference.html#api).


## CLI command
The [Rimu CLI
command](https://srackham.github.io/rimu/reference.html#rimuc-command) installed
by Pipkis `rimupy`.

You could also run it with `python3 -m rimuc`.


## Building
To build from source:

1. Clone source repo from Github:

        git clone git@github.com:srackham/rimu-py.git

2. Create and initialize virtual environment:

        cd rimu-py/
        make init

3. Activate virtual environment:

        source .venv/bin/activate

4. Test and build:

        make build


## Learn more
Read the [documentation](https://srackham.github.io/rimu/reference.html) and experiment
with Rimu in the [Rimu
Playground](http://srackham.github.io/rimu/rimuplayground.html).


## Implementation
- The largely one-to-one correspondence between the canonical
  [TypeScript code](https://github.com/srackham/rimu) and the Python code
  eased porting and debugging.  This will also make it easier to
  cross-port new features and bug-fixes.

- All Rimu implementations share the same JSON driven test suites
  comprising over 300 compatibility checks.