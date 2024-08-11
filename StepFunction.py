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
