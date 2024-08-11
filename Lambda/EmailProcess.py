import json
import boto3
import logging

# SES 클라이언트 초기화
ses_client = boto3.client('ses', region_name='ap-northeast-2')  # 적절한 리전 지정

def send_email(recipient, subject, body):
    try:
        # SES를 사용하여 이메일 전송
        response = ses_client.send_email(
            Source='ldj990517@gmail.com',  # AWS SES에서 인증한 발신자 이메일 주소
            Destination={
                'ToAddresses': [recipient]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {
                        'Data': body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        return response['MessageId']  # 이메일 전송 성공시 메시지 ID 반환
    except Exception as e:
        logging.error(f"Error sending email to {recipient}: {str(e)}")
        raise

def lambda_handler(event, context):
    # 이벤트로부터 템플릿 및 사용자 데이터 추출
    print(event)
    body = json.loads(event['body'])
    template = body['template']
    user = body['user']
    results = []
    print(user)
    # 각 사용자에 대한 이메일 생성 및 전송
    
    personalized_subject = user['Subject']  # 실제 제목 (추가 처리 가능)
    personalized_body = template['body'].replace('{{Name}}', user['Name']).replace('{{Body}}', user['Body'])
        
    #     # 이메일 전송
    message_id = send_email(user['Email'], personalized_subject, personalized_body)
    results.append({'Email': user['Email'], 'MessageId': message_id})

    # 모든 이메일 전송 결과 로깅
    logging.info(f"All emails sent successfully: {results}")

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Emails sent successfully', 'details': results})
    }

