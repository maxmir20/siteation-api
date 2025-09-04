from fastapi import FastAPI
import boto3
from boto3.dynamodb.conditions import Key
from urllib.parse import urlparse

app = FastAPI()
dynamodb = boto3.resource('dynamodb')
table =dynamodb.Table('siteations')



@app.get("/exists/")
def siteation_domain_exists(url):
    domain = urlparse(url).netloc

    if not domain:
        return {"status_code": 400, "message":"Invalid URL"}

    result = table.query(
        KeyConditionExpression=Key('domain').eq(domain),
        Limit=1
    )

    return {"status_code": 200, "exists": bool(result['Items'])}
            


@app.get("/value/")
def get_siteation_value(url):
    domain, path = urlparse(url).netloc, urlparse(url).path

    if not domain:
        return {"status_code": 400, "message":"Invalid URL"}

    result = table.get_item(
        Key={
            'domain': domain,
            'path': path
        }
    )

    if not result['Item']:
        return {"status_code": 404}

    return {"status_code": 200, "message":result['Item']['site_value']}
    
    

@app.patch("/add/")
def update_siteation_value(url):
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