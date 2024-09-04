# Banodora-Bot
![W5LZnYKESz6Vyd2W5xCLJg](https://github.com/user-attachments/assets/e216b000-f1ee-4b94-b294-e34b4ca4d4c0)

# Setup
install the python packages:
```python
pip install -r requirements.txt
```
Rename the .env file
```python
.env.example -> .env
```
Fill out the env vars
```python
BOT_TOKEN=
TEXT_GENERATION_URL=
```
Run the bot
```python
python3 scripts/main.py
```
It also includes a dockerfile for running it in the cloud
```python
docker build -t bandoco-bot:latest .
```
