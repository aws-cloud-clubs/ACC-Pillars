import mysql.connector
import boto3
from botocore.exceptions import ClientError
import csv
import json
import tempfile
import os

def export_data_to_s3():
    # MySQL 데이터베이스 연결 설정
    db = mysql.connector.connect(
        host = os.environ.get('HOST'),
        user= os.environ.get('USER'),
        password = os.environ.get('PASSWORD'),
        database = os.environ.get('DATABASE')
    )

    cursor = db.cursor()

    # MySQL 쿼리 실행
    cursor.execute("SELECT id, name, email, created_at, gender FROM users")
    rows = cursor.fetchall()

    # DynamoDB 클라이언트 설정
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
    table = dynamodb.Table('User')
    
    batch_size = 25
    batch_data = []
    
    for row in rows:
        item = {
            'Email': row[2],
            'Name': row[1],
            'CreateTime': row[3].strftime('%Y-%m-%d %H:%M:%S') if row[3] else None,
            'Gender': row[4],
            'SubscriptionStatus': 'true'
        }
        batch_data.append(item)
        
        if len(batch_data) == batch_size:
            write_to_dynamodb(table, batch_data)
            batch_data = []
    
    # 남은 데이터 처리
    if batch_data:
        write_to_dynamodb(table, batch_data)


    # 연결 종료
    cursor.close()
    db.close()

    print("Data export to S3 completed successfully.")

def write_to_dynamodb(table, items):
    with table.batch_writer() as batch:
        for item in items:
            try:
                batch.put_item(Item=item)
            except ClientError as e:
                print(f"Error inserting item with Email: {item['Email']} - {e}")



if __name__ == "__main__":
    migrate_data()
