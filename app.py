from flask import Flask, request, jsonify
import requests
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# =============================
# CONFIG
# =============================

SERVICENOW_INSTANCE = os.getenv("SERVICENOW_INSTANCE")
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")

OLLAMA_URL = "http://localhost:11434/api/generate"

# =============================
# SAFE RESPONSE WRAPPER
# =============================

def safe_response(mode="error", data=None, error=None):
    return jsonify({
        "mode": mode,
        "data": data,
        "error": error
    })

# =============================
# OLLAMA
# =============================

def ask_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
        )

        if response.status_code != 200:
            return f"Ollama error: {response.text}"

        return response.json().get("response", "")

    except Exception as e:
        return f"Ollama exception: {str(e)}"

# =============================
# SERVICENOW
# =============================

def get_incident(number):
    try:
        url = f"{SERVICENOW_INSTANCE}/api/now/table/incident"
        params = {"sysparm_query": f"number={number}"}
        response = requests.get(
            url,
            auth=(USERNAME, PASSWORD),
            params=params
        )

        if response.status_code != 200:
            return None, response.text

        return response.json(), None

    except Exception as e:
        return None, str(e)

def get_similar_incidents(short_desc, category):
    try:
        url = f"{SERVICENOW_INSTANCE}/api/now/table/incident"
        query = f"short_descriptionLIKE{short_desc}^category={category}"
        params = {"sysparm_query": query, "sysparm_limit": 5}

        response = requests.get(
            url,
            auth=(USERNAME, PASSWORD),
            params=params
        )

        if response.status_code != 200:
            return {}

        return response.json()

    except:
        return {}

def create_incident(short_description, description, category):
    try:
        url = f"{SERVICENOW_INSTANCE}/api/now/table/incident"
        payload = {
            "short_description": short_description,
            "description": description,
            "category": category
        }

        response = requests.post(
            url,
            auth=(USERNAME, PASSWORD),
            json=payload
        )

        if response.status_code not in [200, 201]:
            return None, response.text

        return response.json(), None

    except Exception as e:
        return None, str(e)

# =============================
# AI ANALYSIS
# =============================

def generate_analysis(incident, similar_incidents):

    prompt = f"""
You are an Enterprise ITSM AI System.

Current Incident:
{incident}

Similar Historical Incidents:
{similar_incidents}

Generate:

1. Incident Summary
2. Root Cause
3. Recommended Resolution
4. Troubleshooting Steps
5. Confidence Score (0-100%)

Use historical patterns only.
"""

    return ask_ollama(prompt)

# =============================
# MAIN ROUTE
# =============================

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return safe_response("error", error="Empty request.")

        # CREATE INCIDENT FLOW
        if "create incident" in user_message.lower():

            prompt = f"""
Extract short_description, description and category from:
{user_message}

Return valid JSON only:
{{
  "short_description": "...",
  "description": "...",
  "category": "..."
}}
"""

            structured = ask_ollama(prompt)

            try:
                parsed = json.loads(structured)
            except:
                return safe_response("error", error="Failed to parse creation request.")

            created, err = create_incident(
                parsed.get("short_description", "AI Generated Incident"),
                parsed.get("description", user_message),
                parsed.get("category", "General")
            )

            if err:
                return safe_response("error", error=err)

            return safe_response("create", data=created)

        # ANALYZE INCIDENT FLOW
        match = re.search(r"INC\d+", user_message)

        if not match:
            return safe_response("error", error="No incident number found.")

        incident_number = match.group()

        incident_data, err = get_incident(incident_number)

        if err:
            return safe_response("error", error=err)

        if not incident_data or not incident_data.get("result"):
            return safe_response("error", error="Incident not found.")

        incident = incident_data["result"][0]
        category = incident.get("category", "General")
        short_desc = incident.get("short_description", "")

        similar = get_similar_incidents(short_desc, category)

        analysis = generate_analysis(incident, similar)

        return safe_response("analyze", data={
            "incident_number": incident_number,
            "category": category,
            "analysis": analysis
        })

    except Exception as e:
        return safe_response("error", error=str(e))

# =============================
# GLOBAL ERROR HANDLER
# =============================

@app.errorhandler(Exception)
def handle_global_error(e):
    return safe_response("error", error=str(e)), 500

# =============================
# RUN
# =============================

if __name__ == "__main__":
    app.run(port=5000, debug=True)
