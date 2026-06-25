from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os
import re
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class Query(BaseModel):
    situation: str
    location: str
    language: str = "English"

class ApplyRequest(BaseModel):
    resource_name: str
    situation: str
    language: str = "English"

@app.post("/find-resources")
def find_resources(query: Query):
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": f"""You are a compassionate social services navigator.
A person in {query.location} has described their situation: "{query.situation}"

Respond entirely in {query.language}.

Provide 5-6 specific, actionable resources they can access right now.
For each resource provide exactly these fields with no markdown, no asterisks:

NAME: [resource name]
HELPS WITH: [one plain sentence]
HOW TO ACCESS: [phone, website, or address]
WHO QUALIFIES: [one plain sentence]
URGENCY: [exactly one of: IMMEDIATE, APPLY SOON, ADDITIONAL SUPPORT]
REASON: [one sentence explaining why this matches their specific situation]

Separate each resource with a blank line.
No asterisks, no markdown, no intro paragraph, no closing paragraph."""
            }
        ]
    )

    raw = message.content[0].text
    resources = []
    blocks = re.split(r'\n\s*\n', raw.strip())

    for block in blocks:
        if 'NAME:' not in block.upper():
            continue
        resource = {}
        lines = block.strip().split('\n')
        for line in lines:
            line = re.sub(r'\*+', '', line).strip()
            upper = line.upper()
            if upper.startswith('NAME:'):
                resource['name'] = line.split(':', 1)[1].strip()
            elif upper.startswith('HELPS WITH:'):
                resource['helps_with'] = line.split(':', 1)[1].strip()
            elif upper.startswith('HOW TO ACCESS:'):
                resource['how_to_access'] = line.split(':', 1)[1].strip()
            elif upper.startswith('WHO QUALIFIES:'):
                resource['who_qualifies'] = line.split(':', 1)[1].strip()
            elif upper.startswith('URGENCY:'):
                resource['urgency'] = line.split(':', 1)[1].strip().upper()
            elif upper.startswith('REASON:'):
                resource['reason'] = line.split(':', 1)[1].strip()
        if len(resource) >= 4:
            resources.append(resource)

    # Sort by urgency
    urgency_order = {'IMMEDIATE': 0, 'APPLY SOON': 1, 'ADDITIONAL SUPPORT': 2}
    resources.sort(key=lambda r: urgency_order.get(r.get('urgency', 'ADDITIONAL SUPPORT'), 2))

    return {"resources": resources}

@app.post("/help-apply")
def help_apply(req: ApplyRequest):
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": f"""A person needs help contacting "{req.resource_name}" about their situation: "{req.situation}"

Write a short, clear script in {req.language} they can read aloud when they call, or paste into an email or form.
It should sound human, warm, and honest — not robotic.
Include: who they are, what they need, and a polite ask for help.
Keep it under 100 words. No intro, just the script itself."""
            }
        ]
    )
    return {"script": message.content[0].text.strip()}

@app.get("/")
def root():
    return {"message": "CivicAid API is running"}