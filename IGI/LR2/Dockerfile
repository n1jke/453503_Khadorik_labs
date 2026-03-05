FROM python:3.10-slim

WORKDIR /app

ENV RADIUS=1 SIDE=1

COPY main.py ./main.py
COPY geometric_lib ./geometric_lib

CMD ["python", "main.py"]
