
import boto3
import requests
# 必要モジュールのインポート
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

AWS_HOST_ZONE_ID=os.environ['AWS_HOST_ZONE_ID']
AWS_RECORD_NAME=os.environ['AWS_RECORD_NAME']
AWS_ACCESS_KEY=os.environ['AWS_ACCESS_KEY']
AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']

client = boto3.client('route53', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

print(f'AWS_HOST_ZONE_ID:{AWS_HOST_ZONE_ID}')

# get_route53 = client.get_hosted_zone(
#   Id=AWS_HOST_ZONE_ID
# )

# print(f'get_route53:{get_route53}')

response = client.list_resource_record_sets(
    HostedZoneId=AWS_HOST_ZONE_ID,
    StartRecordName=AWS_RECORD_NAME,
    StartRecordType='A',
    MaxItems='1'
)

print(f'response:{response}')

# now_ip=response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
# new_ip=requests.get("http://httpbin.org/ip").json()['origin']

# if now_ip != new_ip:
#     response = client.change_resource_record_sets(
#         HostedZoneId=AWS_HOST_ZONE_ID,
#         ChangeBatch={
#             'Changes': [
#                 {
#                     'Action': 'UPSERT',
#                     'ResourceRecordSet': {
#                         'Name': AWS_RECORD_NAME,
#                         'Type': 'A',
#                         'TTL': 60,
#                         'ResourceRecords': [
#                             {
#                                 'Value': new_ip
#                             },
#                         ],
#                     }
#                 },
#             ]
#         }
#     )