


# create virtualenv & install dependencies
```bash
mkvirtualenv .env -p python3.5
pip install -r requirements.txt
```

# updating the requirements.txt

This project uses [pip-compile](https://pypi.python.org/pypi/pip-tools/) tool to generate `requirements.txt` with 
all project dependencies (and all underlying dependencies) pinned.

If you decide to add new dependency to the project, simply add it to the `requirements.in` and then regenerate 
`requirements.txt` with `pip-compile`:

```bash
pip install pip-tools
pip-compile
```
