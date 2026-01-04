from fastapi import FastAPI

app = FastAPI(title="{{cookiecutter.project_name}}")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
