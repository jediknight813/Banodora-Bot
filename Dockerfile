FROM python:3.9.9-bullseye

WORKDIR /src

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY scripts ./scripts/
COPY .env ./

ENTRYPOINT ["python3", "scripts/main.py"]

# docker build -t bandoco-bot:latest .

