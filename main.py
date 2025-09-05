from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import boto3
from boto3.dynamodb.conditions import Key
from urllib.parse import urlparse

app = FastAPI()

origins = [
    "chrome-extension://hcnolaabbdkcpkljahjnfhbmogfgoglo"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dynamodb = boto3.resource('dynamodb')
table =dynamodb.Table('siteations')



@app.get("/exists/")
def siteation_domain_exists(url):
    try:
        domain = urlparse(url).netloc

        if not domain:
            return {"status_code": 400, "message":"Invalid URL"}

        result = table.query(
            KeyConditionExpression=Key('domain').eq(domain),
            Limit=1
        )

        return {"status_code": 200, "exists": bool(result['Items'])}
    
    except Exception as e:
        print(f"DynamoDB error in exists check: {e}")
        return {"status_code": 500, "message": "Internal server error"}
            


@app.get("/value/")
def get_siteation_value(url):
    domain, path = urlparse(url).netloc, urlparse(url).path

    if not domain:
        return {"status_code": 400, "message":"Invalid URL"}

    try:
        result = table.get_item(
            Key={
                'domain': domain,
                'path': path
            }
        )

        if 'Item' not in result:
            return {"status_code": 404}
        
        return {"status_code": 200, "site_value":result['Item']['site_value']}
    
    except Exception as e:
        print(f"DynamoDB error: {e}")
        return {"status_code": 500, "message": "Internal server error"}
    

@app.patch("/add/")
def update_siteation_value(url):
    try:
        domain, path = urlparse(url).netloc, urlparse(url).path

        if not domain:
            return {"status_code": 400, "message":"Invalid URL"}

        table.update_item(
            Key={
                'domain': domain,
                'path': path
            },
            UpdateExpression='ADD site_value :val',
            ExpressionAttributeValues={
                ':val': 1
            }
        )
        return {"status_code": 200}
    
    except Exception as e:
        print(f"DynamoDB error in update: {e}")
        return {"status_code": 500, "message": "Internal server error"}