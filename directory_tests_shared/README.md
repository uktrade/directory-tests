Shared resources for Directory Tests
------------------------------------

This package contains various resources used in:
* smoke
* functional
* load
* browser
tests.

# Usage

```python
from directory_tests_shared import settings, URLs
from directory_tests_shared.enums import BusinessType
```


# Pycharm

In order to force PyCharm to find `directory_tests_shared` package,
go to `Settings` -> `Project` -> `Project Structure` and
mark `directory_tests_shared` folder as `Sources`.

![Mark directory_tests_shared directory as Sources](./pycharm_sources.png)
