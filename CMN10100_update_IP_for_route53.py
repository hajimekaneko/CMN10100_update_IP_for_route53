
import boto3
import requests
import re
# 必要モジュールのインポート
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

DEBUG_=os.environ['DEBUG']

AWS_HOST_ZONE_ID=os.environ['AWS_HOST_ZONE_ID']
AWS_RECORD_NAME=os.environ['AWS_RECORD_NAME']
if not DEBUG_:
    AWS_ACCESS_KEY=os.environ['AWS_ACCESS_KEY_DEV']
    AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY_DEV']  
    print("PROD")
else:
    AWS_ACCESS_KEY=os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_ACCESS_KEY=os.environ['AWS_SECRET_ACCESS_KEY']
    print("DEV")

AWS_CLOUDFRONT_DESTRIBUTION_ID='E2GBZVMGSQ573N'

boto3_session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
cf_client = boto3_session.client('cloudfront')

# Distribution ID を指定して Distribution を取得
dist = cf_client.get_distribution(Id=AWS_CLOUDFRONT_DESTRIBUTION_ID)

# Distribution Config から Origin を取得
origins = dist['Distribution']['DistributionConfig']['Origins']['Items']

# Origin から Domain Name を取得
origin_domain = origins[0]['DomainName']
# Origin から Origin ID を取得
origin_id = origins[0]['Id']

# Domain Name からホスト名を取得
match = re.search(r'://(.+?)/', origin_domain)
origin_host = match.group(1)

print("Origin Host: {}".format(origin_host))


# 変更内容を辞書型で定義
updated_origin = {
    'Id': origin_id,
    'DomainName': '[更新後のオリジンのドメイン名]',
    'CustomOriginConfig': {
        'OriginProtocolPolicy': 'https-only',
        'OriginSslProtocols': {
            'Quantity': 1,
            'Items': [
                'TLSv1.2'
            ]
        }
    }
}

# Distribution の Origin を更新
cf_client.update_distribution(
    DistributionConfig={
        'Origins': {
            'Quantity': 1,
            'Items': [
                updated_origin
            ]
        }
    },
    Id='[Distribution ID]',
    IfMatch=dist['ETag']
)


# client = boto3.client('cloudfront', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# print(f'AWS_HOST_ZONE_ID:{AWS_HOST_ZONE_ID}')

# # get_route53 = client.get_hosted_zone(
# #   Id=AWS_HOST_ZONE_ID
# # )

# # print(f'get_route53:{get_route53}')

# response = client.list_resource_record_sets(
#     HostedZoneId=AWS_HOST_ZONE_ID,
#     StartRecordName=AWS_RECORD_NAME,
#     StartRecordType='A',
#     MaxItems='1'
# )

# now_ip=response['ResourceRecordSets'][0]['ResourceRecords'][0]['Value']
# # new_ip=requests.get("http://httpbin.org/ip").json()['origin']

# print(f'now_ip:{now_ip}')

# # if now_ip != new_ip:
# #     response = client.change_resource_record_sets(
# #         HostedZoneId=AWS_HOST_ZONE_ID,
# #         ChangeBatch={
# #             'Changes': [
# #                 {
# #                     'Action': 'UPSERT',
# #                     'ResourceRecordSet': {
# #                         'Name': AWS_RECORD_NAME,
# #                         'Type': 'A',
# #                         'TTL': 60,
# #                         'ResourceRecords': [
# #                             {
# #                                 'Value': new_ip
# #                             },
# #                         ],
# #                     }
# #                 },
# #             ]
# #         }
# #     )