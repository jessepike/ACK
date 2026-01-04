{% if cookiecutter.project_type == "python_fastapi_api" %}
FROM python:{{cookiecutter.python_version}}-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn","src.app:app","--host","0.0.0.0","--port","8000"]
{% elif cookiecutter.project_type == "node_nextjs_app" %}
FROM node:{{cookiecutter.node_version}}-bookworm-slim
WORKDIR /app
COPY package.json .
# lockfile handled by your package manager
COPY . .
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm","run","start"]
{% else %}
FROM alpine:3.19
CMD ["sh","-lc","echo 'No docker image for this project type' && sleep 3600"]
{% endif %}
