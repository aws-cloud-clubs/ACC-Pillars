import boto3
import json

from decimal import Decimal

def lambda_handler(event, context):
    # DynamoDB 테이블에 연결
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('User')
    
    # event에서 LastEvaluatedKey를 가져옵니다. 없으면 빈 딕셔너리로 초기화합니다.
    last_evaluated_key = event.get('LastEvaluatedKey', {})
    
    # 테이블에서 최대 10개 항목 가져오기
    scan_params = {
        'Limit': 10,
        'ProjectionExpression': "#name, Gender, SubscriptionStatus, Email",
        'ExpressionAttributeNames': {
            "#name": "Name"
        }
    }
    
    # LastEvaluatedKey를 ExclusiveStartKey로 설정하여 페이지네이션을 수행합니다.
    if last_evaluated_key:
        scan_params['ExclusiveStartKey'] = last_evaluated_key
   
    
    # DynamoDB 스캔 작업 수행
    response = table.scan(**scan_params)
    print(response.get('LastEvaluatedKey'))
    
    # Decimal을 float로 변환하는 함수
    def decimal_to_float(item):
        if isinstance(item, dict):
            return {k: decimal_to_float(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [decimal_to_float(i) for i in item]
        elif isinstance(item, Decimal):
            return float(item)
        else:
            return item
    
    # Decimal을 float로 변환
    items = decimal_to_float(response.get('Items', []))
    
    # 디버깅을 위한 로그 추가
    print("Items retrieved from DynamoDB:", json.dumps(items))
    
    # 결과 반환
    return {
        'Payload': items,
        'LastEvaluatedKey': response.get('LastEvaluatedKey')  # 다음 페이지를 위한 LastEvaluatedKey 반환
    }
