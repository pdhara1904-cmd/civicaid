# CivicAid

**Find local help, instantly — no forms, no runaround.**

CivicAid is an AI-powered resource navigator that helps people in crisis find real local support programs — food assistance, emergency housing, legal aid, medical care, and more — in seconds. Built with Claude AI, it translates complex government and nonprofit services into plain language anyone can understand, in 24 languages.

🌐 **Live App:** [civicaid-zeta.vercel.app](https://civicaid-zeta.vercel.app)

---

## The Problem

When someone loses their job, faces eviction, or needs urgent help, they're sent to a maze of government websites, disconnected hotlines, and confusing eligibility forms. People in crisis don't have time to navigate bureaucracy — they need answers now.

CivicAid solves this by letting anyone describe their situation in plain English (or their own language), and instantly surfaces the most relevant, actionable local resources — ranked by urgency, with specific contact information and a script to help them apply.

---

## Features

**AI-Powered Resource Matching**
Describe your situation in plain language. Claude analyzes your specific circumstances — job loss, dependents, location, housing status — and returns the most relevant resources, not just keyword matches.

**Urgency Triage**
Every resource is tagged as Immediate Action, Apply Soon, or Additional Support so users know exactly where to start when time matters most.

**Why This Matches You**
Each result explains specifically why it was recommended based on the user's situation — building trust and reducing confusion.

**Help Me Apply**
One click generates a personalized script the user can read aloud on the phone or paste into an application form — removing the barrier of not knowing what to say.

**View on Map**
Every resource links directly to Google Maps so users can see exactly where to go.

**24 Languages**
Full support for English, Spanish, Hindi, Gujarati, Mandarin, Cantonese, Arabic, French, Portuguese, Russian, Korean, Vietnamese, Tagalog, Polish, Haitian Creole, Urdu, Bengali, Punjabi, Italian, German, Japanese, Swahili, Somali, and Amharic — covering the most underserved immigrant and refugee communities in the US.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React, TypeScript |
| Backend | Python, FastAPI |
| AI | Anthropic Claude API |
| Deployment | Vercel (frontend), Railway (backend) |

---

## How It Works

1. User describes their situation in their own words and selects their language
2. FastAPI backend sends the situation and location to Claude with a structured prompt
3. Claude returns 5-6 specific local resources with urgency levels and personalized reasoning
4. Frontend renders results as clean, actionable cards
5. User can generate an application script or open the resource in Google Maps

---

## Running Locally

**Prerequisites:** Python 3.9+, Node.js 18+, Anthropic API key

**Backend**
```bash
cd backend
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key_here" > .env
uvicorn main:app --reload
```

**Frontend**
```bash
cd frontend
npm install
npm start
```

App runs at `http://localhost:3000`

---

## Project Structure

```
civicaid/
├── backend/
│   ├── main.py          # FastAPI app with /find-resources and /help-apply endpoints
│   └── requirements.txt
└── frontend/
    └── src/
        └── App.tsx      # Full React app with multilingual support
```

---

## Why I Built This

Navigating social services in America is unnecessarily hard — especially for people who don't speak English fluently, aren't familiar with the system, or are dealing with a crisis for the first time. I built CivicAid to make that first step easier: describe what you're going through, and get real help, right now.

---

## Future Roadmap

- SMS interface for users without smartphones
- Integration with 211 database for verified real-time resource availability
- Saved sessions so users can return to their resource list
- Nonprofit dashboard for organizations to track community needs

---

*Built with Claude AI by Dhara Patel*
