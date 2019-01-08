## Asynchronous FastROCS v.2 (Flask + FastROCS)

### INSTALLATION

All the prerequisites can be installed via conda command.

```
conda install -c openeye openeye-toolkits
conda install flask-socketio gevent cffi
```

Then, install the asyncfastrocs package.

```
pip install --upgrade asyncfastrocs-VER-py3-none-any.whl
```

### Create initial database

```
mkdir newdir
cd newdir
python -m asyncfastrocs.initialize
```

### Running server

```
FLASK_APP=asyncfastrocs.app flask run --host 0.0.0.0 >> LOG 2>&1 &
disown
```
