import hashlib
import hmac
import json
import os
from enum import Enum

import validators

from typing import Annotated
from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

import boto3
from boto3.dynamodb.conditions import Key
from urllib.parse import urlparse

load_dotenv()
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET').encode("utf-8")

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
table = dynamodb.Table('siteations')


class GithubPullRequest(str, Enum):
    pull_request = "pull_request"


async def validate_github_request(
        request: Request,
        x_github_event: Annotated[GithubPullRequest, Header()],
        x_hub_signature_256: Annotated[str, Header()]):
    body = await request.body()

    is_valid = verify_signature(body, x_hub_signature_256)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Site-ation only accepts properly encrypted file")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    return payload


@app.get("/exists/")
def siteation_domain_exists(url):
    domain = urlparse(url).netloc
    if not domain:
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:
        result = table.query(
            KeyConditionExpression=Key('domain').eq(domain),
            Limit=1
        )

        return {"status_code": 200, "exists": bool(result['Items'])}
    except Exception:
        raise HTTPException(status_code=500, detail="Error occurred when accessing DynamoDB")
            

@app.get("/value/")
def fetch_siteation_value(url):
    parsed_url = urlparse(url)
    domain, path = parsed_url.netloc, parsed_url.path
    if not domain:
        raise HTTPException(status_code=400, detail="Invalid URL")

    try:
        result = table.get_item(
            Key={
                'domain': domain,
                'path': path
            }
        )

        if 'Item' not in result:
            raise HTTPException(status_code=404, detail="Site not found")
        
        return {"status_code": 200, "site_value": result['Item']['site_value']}
    except Exception:
        raise HTTPException(status_code=500, detail="Error occurred when accessing DynamoDB")


@app.post("/webhook")
async def maybe_add_siteation(request_payload: Annotated[dict, Depends(validate_github_request)]):
    pull_request_body = request_payload.get('pull_request', {}).get('body')

    siteation_urls = parse_valid_siteations(pull_request_body)

    update_siteation_values(siteation_urls)

    return {"status_code": 201, "siteations_updated": siteation_urls}


def verify_signature(body, signature):
    if not signature:
        return False

    if not signature.startswith("sha256="):
        return False

    _, signature = signature.split('=')
    expected_signature = hmac.new(WEBHOOK_SECRET, body, hashlib.sha256).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


#  Need to update individually because there is no batchUpdateItem API
#  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_BatchWriteItem.html
def update_siteation_values(siteation_urls):
    try:
        for url in siteation_urls:
            parsed_url = urlparse(url)
            domain, path = parsed_url.netloc, parsed_url.path

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
        return
    except Exception:
        raise HTTPException(status_code=500, detail="Error occurred while updating DynamoDB")


def parse_valid_siteations(pull_request_body):
    siteation_urls = []
    if not pull_request_body:
        return siteation_urls

    try:
        _, siteations = pull_request_body.split("[Site-ations]", 1)
        siteation_lines = [line.strip() for line in siteations.splitlines() if line.strip()]

        for line in siteation_lines:
            _, url = line.split(" ", 1)
            if not validators.url(url):
                continue

            siteation_urls.append(url)
    except ValueError:  # error parsing our siteation line
        print("we made a mistake somewhere")
        pass

    return siteation_urls
