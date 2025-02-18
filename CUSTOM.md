## Customized Features

- **Django_admin_log**: 


## PyPi

change detail in pyproject.toml

```bash
virtualenv venv
source venv/bin/activate

pip install setuptools wheel twine build
```

```bash
git fetch

python -m build  
twine upload dist/*
```