# Pony Express - a chat application

## Backend

The backend of the application is written in python using the
[https://fastapi.tiangolo.com/](FastAPI) framework.

### Setup/Development
If you are using `poetry`, the dependencies may be installed as follows.
```bash
poetry install
```
Make sure that your IDE is setup to use the poetry virtual environment.  If you use
VSCode, you can run
```bash
poetry run code .
```
to start the application or you may connect the virtual environment manually.

If you are managing your virtual environment with `venv`, make sure you build and activate
your virtual environment as specified. With your virtual environment activated, the
dependencies may be installed as follows.
```bash
python -m pip install -r requirements.txt
```
Make sure that your IDE is setup to use the virtual environment. If you use VSCode, you
can run
```bash
code .
```
while the virtual environment is activated or you may connect the virtual environment
manually.

### Running the server locally
If you are using poetry, the local server can be started as follows.
```bash
poetry run uvicorn backend.main:app --reload
```

If you are using a virtual environment, the local server can be started from within the
virtual environment as follows.
```bash
uvicorn backend.main:app --reload
```

Now you should be able to make requests against `http://127.0.0.1:8000` to test your API
locally. You can also inspect the documentation using one of the following:
- swagger at `http://127.0.0.1:8000/docs`
- redoc at `http://127.0.0.1:8000/redoc`

