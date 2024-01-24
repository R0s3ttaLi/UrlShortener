FROM python:3.9-alpine3.17
WORKDIR /app
COPY requirements.txt .
COPY backend /app/backend
RUN  pip install -r requirements.txt
CMD ["flask", "--app", "backend", "run", "--host=0.0.0.0"]
EXPOSE 5000

