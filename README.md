# Real-Time ChatApplication With Django (Channels)
A simple chat-application with channels written in **Synchronous** and **WebSocket Protocol**.

## Usage :
##### 1 - Install requirements lib
```bash
pip install requirements.txt
```
##### 2 - Run redis on Docker
```
docker pull redis
docker run -p 6379:6379 --name redis-chat redis
```
##### 3 - Create database and table
```bash
python manage.py makemigrations
python manage.py migrate --sync-db
```

##### 4 - Go to ```localhost/``` and log in, then enter any room_name to join it.

---

**You can test this chat-app between two user and chat with each other and even send photos**!