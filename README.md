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


## ❔ AWS Services Usage Explanations 
- StepFunction
- Email Verification(sandbox)
- Lambda
- DynamoDB




## 🛠 Overall Project Structure Diagram
<img width="914" alt="AWS 구조도" src="https://github.com/user-attachments/assets/f7638310-3dc0-4970-a5f5-7b0f71334790">

## 🛠 StepFunction Flow
<img width="349" alt="stepfunction flow" src="https://github.com/user-attachments/assets/af3c839c-602f-4aac-a89b-3990a0e5c0cc">

## 🎯 Key Code Explanations
- 설명은 주석처리 해두었습니다. 
- Lambda #1
    -
    ```python
    
    ```

- Lambda #2
    -
    ```python
    
    ```

- Lambda #3
    -
    ```python
    
    ```

- StepFunction
    -
    ```python
    
    ```
## 🔗 기술 블로그 링크



## 🔗 최종 보고서 링크







