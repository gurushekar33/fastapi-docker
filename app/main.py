from fastapi import FastAPI, HTTPException
import pymysql
from pymongo import MongoClient
import redis
from dotenv import load_dotenv
import os
 
app = FastAPI()
 
# Load environment variables from .env file
load_dotenv()
 
# MySQL Configuration
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
 
# MongoDB Configuration
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))
 
# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
 
# Check MySQL connection
def check_mysql():
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            connect_timeout=5
        )
        connection.close()
        return True
    except pymysql.MySQLError:
        return False
 
# Check MongoDB connection
def check_mongo():
    try:
        client = MongoClient(host=MONGO_HOST, port=MONGO_PORT, serverSelectionTimeoutMS=5000)
        client.server_info()
        return True
    except Exception:
        return False
 
# Check Redis connection
def check_redis():
    try:
        client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=5)
        client.ping()
        return True
    except redis.exceptions.ConnectionError:
        return False
 
# Health check endpoint
@app.get("/health")
async def health_check():
    status = {
        "mysql": check_mysql(),
        "mongo": check_mongo(),
        "redis": check_redis()
    }
    # if False in status.values():
    #     raise HTTPException(status_code=503, detail="One or more services are unavailable")
    return {"status": "ok", "services": status}