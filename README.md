<h2 align="center"> 💇 이메일 대량 발송 시스템 설계</h2>



### 🔗 **Requirements** <br>
- 매일 최대 500건의 이메일 대량 발송 필요
- 이메일당 평균 크기는 100KB 예상
- 이메일 발송 지연 시간은 5분 이내
- 발송 실패 처리: 실패한 이메일에 대한 자동 재시도 로직 (최대 3회)
- 구독 관리: 사용자별 이메일 수신 설정 및 구독 해지 기능
- 스팸 방지: SES의 SPF를 통한 도메인 인증

### 🔗 **User Scenarios** <br>
- 무신사 마케팅 직원 A씨가 고객 200명에게 맞춤형 홍보 이메일 전송



## 👥 Team members

<div align=center> 

  | 박언선 | 김지원 | 박가영 | 이동준 | 정현석 | 황규리|
  | :---: | :---: | :---: | :---: | :---: | :---: |  
  | <img src="https://avatars.githubusercontent.com/eonpark" alt="profile" width="180" height="180"> | <img src="https://avatars.githubusercontent.com/JiwonKim08" alt="profile"   width="180" height="180"> | <img src="https://avatars.githubusercontent.com/ParkIsComing" alt="profile" width="180" height="180"> | <img src="https://avatars.githubusercontent.com/dongjune8931" alt="profile" width="180" height="180">| <img src="https://avatars.githubusercontent.com/Junghs21" alt="profile" width="180" height="180"> | <img src="https://avatars.githubusercontent.com/gyuuuuri" alt="profile" width="180" height="180">|
  | [eonpark](https://github.com/eonpark) | [JiwonKim08](https://github.com/JiwonKim08) | [ParkIsComing](https://github.com/ParkIsComing) | [dongjune8931](https://github.com/dongjune8931)| [Junghs21](https://github.com/Junghs21)| [gyuuuuri](https://github.com/gyuuuuri)|

</div>

## ✨ Technology Stack

<div align=center> 
<img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20EC2-FF9900?style=for-the-badge&logo=Amazon%20EC2&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=Amazon%20S3&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=for-the-badge&logo=Amazon%20DynamoDB&logoColor=white">
<img src="https://img.shields.io/badge/AWS%20Step%20Functions-00B2E5?style=for-the-badge&logo=aws-stepfunctions&logoColor=white">
<img src="https://img.shields.io/badge/AWS%20Lambda-4F5D95?style=for-the-badge&logo=aws-lambda&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20SQS-4B9CDB?style=for-the-badge&logo=Amazon%20SQS&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20CloudWatch-2575E0?style=for-the-badge&logo=Amazon%20CloudWatch&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20SES-FF9900?style=for-the-badge&logo=Amazon%20SES&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20API%20Gateway-003A6C?style=for-the-badge&logo=Amazon%20API%20Gateway&logoColor=white">
<img src="https://img.shields.io/badge/Amazon%20RDS-527FFF?style=for-the-badge&logo=Amazon%20RDS&logoColor=white">
  <br>
</div>


## ❔ **AWS Services Usage Explanations** 
> **Lambda**
  - 15분의 Lambda 실행 시간의 제약 발생
  - but, Serverless 환경의 장점을 사용하고 싶음
  - StepFunction 도입
> **StepFunction**
  
  - Map을 사용해 동일한 워크플로우(예: Lambda 함수 호출)를 병렬로 실행
  - 전체 실행시간을 단축 & 복잡한 반복 로직을 간결하게 처리 
  - 이메일이 늘어날수록 처리속도 상승
> **Email Verification(sandbox)**
-
> **DynamoDB**




## **🛠 Overall Project Structure Diagram**
<img width="914" alt="AWS 구조도" src="https://github.com/user-attachments/assets/f7638310-3dc0-4970-a5f5-7b0f71334790">

## **🛠 StepFunction Map Flow**
<img width="349" alt="stepfunction flow" src="https://github.com/user-attachments/assets/af3c839c-602f-4aac-a89b-3990a0e5c0cc">

## 🎯 **Lambda Explanations**
> **StepFunction 내 Lambda 별 기능 및 Input/Output**

|   | Lambda(1) | Lambda(2) | Lambda(3) |
|---|-----------|-----------|-----------|
| **목적** | 유저리스트 n개씩 가져옴 | payload를 큐로 n개씩 전송 | SQS에서 SES로 이메일 전송 |
| **Input** | 유저리스트 chunk (크기: n개) (DynamoDB에서 유저 데이터 몇 개 읽어올 지) | 유저리스트 데이터 (DynamoDB에서 꺼내온 정보) | 유저 payload 리스트 n개 배치 |
| **Output** | 1. 유저리스트 chunk (DynamoDB에서 꺼내온 정보 = name, email, gender, isscribing) 2. 템플릿 정보 | 유저 payload 리스트 n개 배치 (name, email, subject, body) | 메일 완성본 (템플릿에 유저 payload 삽입 + 구독취소링크 삽입 + S3에서 가져온 이미지 삽입) |



-Lambda (1) - GetUserData
  -
  <strong>Output</strong>
  ```
{
  "result": {
    "Payload": [
      {
        "Gender": "Male",
        "SubscriptionStatus": true,
        "Email": "jiwonkim0810@gmail.com",
	      "Name": "chulsu"
      },
      
        .
        .      (생략)
        .
      
      
      {
        "Gender": "Female",
        "SubscriptionStatus": "true",
        "Email": "yuripark066@gmail.com",
        "Name": "Karen Young"
      },
    ],
    "LastEvaluatedKey": {
      "Email": "yuripark066@gmail.com"
    } 
  }
  ```
  ```
- 10개의 유저데이터 output은 map#1~map#10에 해당
- 들고 온 마지막 데이터를 LastEvaluatedKey 로 저장
  ```

-Lambda (2) - EmailQueuer
  -
<table>
  <tr>
    <td><strong>Input</strong></td>
    <td><strong>Output</strong></td>
  </tr>
  <tr>
    <td>
      <pre>
{
  "Gender": "Female",
  "SubscriptionStatus": "true",
  "Email": "jiwonkim0810@gmail.com",
  "Name": "chulsu"
}
      </pre></br></br></br></br></br></br></br></br><blockquote>
    </td>
    <td>
      <pre>
{
  "statusCode": 200, "body": { "template": { "subject": "환영합니다!", "body": "<!DOCTYPE html><html lang=\"ko\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{{Subject}}</title></head><body><p>안녕하세요, {{Name}}님!</p><p>{{Body}}</p><p><a href=\"https://www.musinsa.com\">지금 쇼핑하기</a></p><p>감사합니다,<br>무신사 팀</p><p>이 메일은 무신사에서 발송되었습니다. 수신 거부를 원하시면 <a href=\"#\">여기</a>를 클릭하세요.</p></body></html>" }, 
  "user": {
     "Email": "jiwonkim0810@gmail.com",
      "Name": "chulsu",
      "Subject": "무신사 파격세일", 
      "Body": "들어가는 말" } }
}
      </pre>
    </td>
  </tr>
</table>

```
- Lambda(2)의 위 포멧은 map#1만을 의미 
- Step Functions의 Map 특성상, 나머지 map#2~map#10도 병렬 처리되고 있음
    → SES에 저장해 둔 템플릿을 가져와 Lambda(3)로 옮김
    → Lambda(3)로 이동 전 SQS 거침
  ```



-Lambda (3) - EmailPayload
  -
  ```
  - 메일 완성본을 SES로 전달
     -> S3으로부터 이미지 삽입
     -> 구독 취소 링크 삽입
  ```

- StepFunction
    -
    ```python
    {
      "StartAt": "Lambda (1)",
      "States": {
        "Lambda (1)": {
          "Type": "Task",
          "Resource": "arn:aws:lambda:ap-northeast-2:008971651769:function:GetUserData10",
          "ResultPath": "$.result",
          "Next": "Map"
        },
        "Map": {
          "Type": "Map",
          "ItemsPath": "$.result.Payload",
          "MaxConcurrency": 10,
          "ItemProcessor": {
            "ProcessorConfig": {
              "Mode": "INLINE"
            },
            "StartAt": "Lambda(2)",
            "States": {
              "Lambda(2)": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:ap-northeast-2:008971651769:function:EmailQueuer_update",
                "Next": "Lambda (3)"
              },
              "Lambda (3)": {
                "Type": "Task",
                "Resource": "arn:aws:states:::lambda:invoke",
                "OutputPath": "$.Payload",
                "Parameters": {
                  "Payload.$": "$",
                  "FunctionName": "arn:aws:lambda:ap-northeast-2:008971651769:function:email_pra"
                },
                "Retry": [
                  {
                    "ErrorEquals": [
                      "Lambda.ServiceException",
                      "Lambda.AWSLambdaException",
                      "Lambda.SdkClientException",
                      "Lambda.TooManyRequestsException"
                    ],
                    "IntervalSeconds": 1,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                  }
                ],
                "End": true
              }
            }
          },
          "Next": "CheckForMoreData",
          "ResultPath": "$.results_test"
        },
        "CheckForMoreData": {
          "Type": "Choice",
          "Choices": [
            {
              "Variable": "$.result.LastEvaluatedKey",
              "IsPresent": true,
              "Next": "UpdateLastEvaluatedKey"
            }
          ],
          "Default": "Finish"
        },
        "UpdateLastEvaluatedKey": {
          "Type": "Pass",
          "Parameters": {
            "LastEvaluatedKey.$": "$.result.LastEvaluatedKey"
          },
          "ResultPath": "$.meta",
          "Next": "Lambda (1)"
        },
        "Finish": {
          "Type": "Succeed"
        }
      }
    }   
     ```

## 🛠 DynamoDB 설계
### [User Table]
- 유저 정보를 저장하기 위한 테이블

**Partition key**
- Email(String)
    - 유저 이메일 주소를 저장하기 위해 사용

**Attributes**
- Name(String)
    - 유저 이름을 저장하기 위해 사용
- Gender(String)
    - 해당 유저의 성별을 저장
- CreateTime(숫자)
    - 회원가입 시간 저장
- SubscriptionStatus(부울)
    - 구독 상태를 저장

### [ImageAndTemplate Table]
- 이메일 템플릿과 사용하는 이미지들의 메타데이터를 저장하기 위한 테이블

**Partition key**
- TemplateID(String)
    - 이메일 템플릿을 고유하게 식별할 TemplateID

**Attributes**
- ImageURLs(List)
    - 해당 템플릿이랑 매핑후, s3에 저장된 해당 이미지 주소
- TemplateName(String)
    - 이메일 템플릿 사용 용도를 간략하게 저장하기 위한 용도






## 🔗 기술 블로그 링크



## 🔗 최종 보고서 링크







