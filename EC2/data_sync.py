import mysql.connector
import boto3
import datetime
import logging
import os
from contextlib import contextmanager

log_file_path = '/home/ubuntu/sync_data.log'
dynamodb_table = 'User'
last_sync_time_file = '/home/ubuntu/last_sync_time.txt'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()  # 콘솔에도 로그를 출력
    ]
)

@contextmanager
def mysql_connection():
    try:
        db = mysql.connector.connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DATABASE')
        )
        yield db
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        raise
    finally:
        db.close()

def get_last_sync_time():
    try:
        with open(last_sync_time_file, 'r') as file:
            return datetime.datetime.fromisoformat(file.read().strip())
    except FileNotFoundError:
        logging.warning("Last sync time file not found. Assuming first run.")
        return datetime.datetime.min
    except ValueError as err:
        logging.error(f"Invalid date format in last sync time file: {err}")
        return datetime.datetime.min

def update_last_sync_time():
    try:
        with open(last_sync_time_file, 'w') as file:
            file.write(datetime.datetime.now().isoformat())
    except Exception as e:
        logging.error(f"Failed to update last sync time: {e}")

def fetch_updated_users(cursor, last_sync_time):
    query = """
    SELECT id, name, email, updated_at, gender, created_at
    FROM users
    WHERE updated_at > %s;
    """
    cursor.execute(query, (last_sync_time,))
    return cursor.fetchall()

def sync_to_dynamodb(users):
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table(dynamodb_table)

    for user in users:
        item = {
            'Email': user[2],
            'Name': user[1],
            'CreateTime': user[5].strftime('%Y-%m-%d %H:%M:%S'),
            'Gender': user[4],
            'SubscriptionStatus': 'true'
        }
        logging.info(f"Putting item: {item}")
        try:
            table.put_item(Item=item)
        except Exception as e:
            logging.error(f"Error putting item {item}: {e}")
    logging.info("Data synchronized to DynamoDB successfully.")

def main():
    last_sync_time = get_last_sync_time()

    with mysql_connection() as db:
        cursor = db.cursor()
        users = fetch_updated_users(cursor, last_sync_time)

        if users:
            sync_to_dynamodb(users)

        cursor.close()

    update_last_sync_time()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Failed to complete sync process: {e}")
