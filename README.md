<h2 align="center"> 📧 이메일 대량 발송 시스템 설계</h2>



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

## **🛠 Structure Diagram Explanations**
![emailprocess](https://github.com/user-attachments/assets/749e3e6f-7297-47dd-aa63-caf2bec8e570)
- 실제 이메일은 sandbox를 해제하지 않는 이상 AWS 계정당 메일 200개만을 보낼 수 있기에, 실행 예시는 200개를 기준으로 함
- DynamoDB에 있는 전체 유저 200명에게 이메일을 보낸다고 가정
- Lambda(1)에서 dynamoDB로부터 10명의 유저 정보를 가져옴
- 그 후 Lambda(2)를 호출해 10명의 유저 payload와 템플릿 정보를 SQS로 전달 (*SQS를 거치는 이유는 이메일 누락을 막기 위함)
- Lambda(3)에서 10명의 유저 payload를 가져와 템플릿에 삽입하여 이메일을 완성한 후, SES로 이메일을 전송
- 200개의 이메일을 전송하기 위해 위 과정을 20번 반복 (10*20 = 200개의 이메일)

## **🛠 StepFunction Map Flow**
<img width="349" alt="stepfunction flow" src="https://github.com/user-attachments/assets/af3c839c-602f-4aac-a89b-3990a0e5c0cc">

## 🛠 AWS SES
> AWS SES(Amazon Simple Email Service)는 대량으로 이메일을 전송할 수 있는 클라우드 이메일 서비스 공급자

- **비용 효율성**: 사용한 만큼만 비용을 지불하여 경제적
- **자동 스케일링**: 이메일 발송 크기가 자동으로 스케일링되어 유연하게 대응
- **상세한 로그와 보고서**: 전송된 이메일에 대한 상세한 로그와 보고서를 제공하여, 다른 서비스의 기준값으로 활용 가능

### 도메인 & 이메일 주소 인증
- **도메인 구매**: 가비아에서 도메인을 구매하여 사용
- **DKIM 인증**: SES에서 제공하는 **DKIM(DomainKeys Identified Mail)**의 CNAME 레코드를 가비아의 도메인 DNS 설정에 추가

    > **목적**: 이메일 전송 시, 도메인이 실제로 내 것임을 증명하고, 이메일이 스팸으로 분류되는 것을 방지
    
<img width="700" alt="자격 증명" src="https://github.com/user-attachments/assets/d1bcea0b-d100-4804-a3b6-34768acf2e64">
    



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

-StepFunction
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

## 🔗 Step Functions Efficiency
<img width="1000" alt="st0" src="https://github.com/user-attachments/assets/d2cbfa3b-6d81-4cef-82cc-1bab1f1396ae">
<img width="1000" alt="step2" src="https://github.com/user-attachments/assets/eef1f1b5-d6d4-498c-8de7-d699e6b7b449">
<img width="1000" alt="step3" src="https://github.com/user-attachments/assets/736dda4f-fdcf-4541-b2a9-a8a8c8b40553">

- 50개의 이메일을 보내는데 총 21초 걸림
- 이를 평균으로 계산하면 5분 동안 보낼 수 있는 이메일의 개수는 750개

## 🔗 development direction
<img width="985" alt="error" src="https://github.com/user-attachments/assets/15d94b1a-46fb-4840-be93-7a70aca668ea">

- Lambda 함수에서 SES에 미리 올려놓은 템플릿을 가져오는 코드에서 너무 많은 API 요청으로 인해 Throttling이 발생 → 이를 해결하기 위해 처음에만 SES에서 템플릿을 가져와서 ElastiCache에 넣어 사용하는 형식으로 위의 문제를 해결하고자 함

## 🛠 DynamoDB 설계
### [User Table]
- 유저 정보를 저장하기 위한 테이블

> **Partition key**
- Email(String)
    - 유저 이메일 주소를 저장하기 위해 사용

> **Attributes**
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

> **Partition key**
- TemplateID(String)
    - 이메일 템플릿을 고유하게 식별할 TemplateID

> **Attributes**
- ImageURLs(List)
    - 해당 템플릿이랑 매핑후, s3에 저장된 해당 이미지 주소
- TemplateName(String)
    - 이메일 템플릿 사용 용도를 간략하게 저장하기 위한 용도




## 📩 이메일 발송을 위한 유저 정보 처리

### 초기에 서비스 운영 DB에서 유저 데이터 가져오기
서비스 운영 DB로 관계형 데이터베이스를 사용하고 있다고 가정하고, 이메일 대량 발송을 위해서는 이메일 보낼 유저의 정보(이름, 이메일, 성별 등)를 관계형 데이터베이스에서 가져

다른 테이블과의 join 작업이 필요하지 않기 때문에 매번 운영 DB에 접속하여 메일을 발송할 유저 정보를 읽어오기 보다는 빠른 Read 작업이 가능한 DynamoDB에 유저 정보를 두고, 메일을 발송할 때 DynamoDB에서 유저 정보를 가져오는 방법이 낫다고 판단하였습니다. 또 주기적으로 운영 DB에서 변동된 유저 정보를 DynamoDB에 업데이트함으로써 데이터를 동일하게 유지합니다.

_* 운영 DB가 RDS에서 MySQL DB를 활용하고 있다고 가정합니다.


초기에는 RDS에 저장된 유저 정보를 S3를 거쳐 DynamoDB에 가져옵니다. 유저 정보가 많은 경우에 대비해 RDS에서 DynamoDB로 한번에 데이터를 옮기지 않고, 데이터를 여러 작은 덩어리로 분할하여 나누어 저장합니다.

### cronjob을 이용한 데이터 동기화
운영 DB에서 유저 정보가 추가, 변경되면서 DynamoDB의 데이터와 달라지면 주기적인 polling을 통해 이를 업데이트 해줘야 합니다. 이메일 발송의 경우, 실시간 동기화가 필요하지 않고 발송 시간을 기준으로 동기화가 되어 있으면 되기 때문에 cronjob을 주기적인 동기화가 이루어지도록 설정했습니다.

**단계**

1. **배치 작업 설정**: 일정 시간 간격(예: 매 시간, 매일)으로 실행되는 배치 작업을 설정합니다.
2. **배치 작업 실행**: EC2 인스턴스에서 주기적으로 배치 스크립트를 실행합니다.
3. **변경된 데이터 추적**: MySQL의 `TIMESTAMP` 타입을 이용하면 데이터가 추가 및 수정될 때 자동으로 `TIMESTAMP` 필드가 업데이트 됩니다. 유저 테이블의 `update_at` 필드를 `TIMESTAMP` 타입으로 설정하여 변경된 데이터를 추적합니다.
4. **데이터 동기화**: 변경된 데이터를 읽어와 DynamoDB에 반영합니다. 이후에도 주기적으로 2~4번 과정이 실행됩니다.








