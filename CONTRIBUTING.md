## Run tests

* setup virtualenv

```bash
python3 -m venv .venv
source./.venv/bin/activate
```

* install requirements
```bash
pip install -r requirements.txt
```
* run tests
```bash
tox # run test matrix
tox -e ansible29-centos7 # Specify test
# Or via molecule
MOLECULE_DISTRO=centos7 molecule test
```


