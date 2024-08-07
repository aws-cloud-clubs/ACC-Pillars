import json
import boto3
import logging

from botocore.exceptions import ClientError

import time


# SES 클라이언트 초기화
ses_client = boto3.client('ses')

# SQS 클라이언트 초기화
sqs_client = boto3.client('sqs')

SQS_QUEUE_URL = 'https://sqs.ap-northeast-2.amazonaws.com/008971651769/emailSendQueue'

def get_email_template_from_ses(template_name):
    try:
        response = ses_client.get_template(TemplateName=template_name)
        template = response.get('Template', {})
        
        # `SubjectPart`는 항상 `template_name`으로 설정
        subject = template_name
        
        # `HtmlPart`는 SES 템플릿에서 가져온 HTML 본문
        body = template.get('HtmlPart', 'Default Body')  
        
        return subject, body
    except Exception as e:
        logging.error(f"Error retrieving template from SES: {str(e)}")
        raise


def get_email_template_from_ses2(template_name):
    retries = 3
    delay = 3  # 초 단위 대기 시간

    for attempt in range(retries):
        try:
            response = ses_client.get_template(TemplateName=template_name)
            subject = response['Template']['SubjectPart']
            body = response['Template']['HtmlPart']
            return subject, body
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2  # 지연 시간 지수적 증가
                else:
                    raise
            else:
                raise

def send_sqs_message(sqs_queue_url, payload):
    try:
        sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=payload
        )
        logging.info("Message sent to SQS successfully.")
    except ClientError as e:
        logging.error(f"Error sending message to SQS: {str(e)}")
        raise

def lambda_handler(event, context):
    # User 리스트를 가져옴
    user = event

    # 이메일 템플릿 이름
    template_name = "ACC_TEST_TEMPLATE"  # 실제 템플릿 이름으로 교체

    # 이메일 템플릿을 가져옴
    subject, body = get_email_template_from_ses2(template_name)
    
    if not body:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Failed to retrieve email template'
            })
        }

    # 유저 정보와 템플릿 정보를 결합하여 결과를 생성
    user_info = {
        'Email': user.get('Email'),
        'Name': user.get('Name'),
        'Subject': "무신사 파격세일",  # SES 템플릿에서 가져온 Subject
        'Body': "들어가는 말"  # SES 템플릿에서 가져온 Body
    }

    result = {
        'template': {
            'subject': subject,
            'body': body
        },
        'user': user_info
    }
    
    # JSON 형식의 문자열로 변환
    email_payload_json = json.dumps(result, ensure_ascii=False)
    
    # SQS에 메시지를 전송
    try:
        send_sqs_message(SQS_QUEUE_URL, email_payload_json)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Failed to send message to SQS: {str(e)}'
            })
        }
    
    # 결과를 반환
    return {
        'statusCode': 200,
        'body': json.dumps(result, ensure_ascii=False)
    }
