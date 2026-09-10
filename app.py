import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel

# 1. Load environment variables from .env file before anything else
load_dotenv()

MODEL = "gemini-3.5-flash-lite" #update with the latest model if needed

app = Flask(__name__)
CORS(app)

# 2. Check for API Key at startup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("\n⚠️ WARNING: GEMINI_API_KEY is not set in environment or .env file!\n")

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

class ProjectIdea(BaseModel):
    project_title: str
    target_audience: str
    difficulty: str
    key_features: list[str]


# ---------------------------------------------------------------------
# ROUTE 1: STRUCTURED JSON (With Error Fallback)
# ---------------------------------------------------------------------
@app.route("/api/json", methods=["POST"])
def generate_json():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({
            "status": "error",
            "message": "Prompt cannot be empty."
        }), 400

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"Generate a hackathon project idea based on: {prompt}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ProjectIdea,
                temperature=0.2,
            ),
        )
        
        parsed_data = json.loads(response.text)
        return jsonify({"status": "success", "data": parsed_data})

    except APIError as e:
        # Catches Google API specific errors (Invalid Key, Quota Exceeded, Rate Limit)
        print(f"\n[GEMINI API ERROR]: {e}")
        return jsonify({
            "status": "error",
            "message": "AI service is currently unavailable or rate limited. Please check your API key and try again."
        }), 502

    except json.JSONDecodeError:
        # Fallback if Gemini output failed to parse into expected JSON
        print("\n[JSON PARSE ERROR]: Gemini returned malformed JSON.")
        return jsonify({
            "status": "error",
            "message": "Failed to parse structured response. Please retry."
        }), 500

    except Exception as e:
        # Catch-all for network issues or unexpected backend errors
        print(f"\n[UNEXPECTED ERROR]: {e}")
        return jsonify({
            "status": "error",
            "message": "Something went wrong on our end. Please try again."
        }), 500


# ---------------------------------------------------------------------
# ROUTE 2: REAL-TIME STREAMING (With Stream Failure Fallback)
# ---------------------------------------------------------------------
@app.route("/api/stream", methods=["POST"])
def generate_stream():
    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return Response("Error: Prompt cannot be empty.", status=400, mimetype="text/plain")

    def generate_chunks():
        try:
            response_stream = client.models.generate_content_stream(
                model=MODEL,
                contents=prompt
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
        except APIError as e:
            print(f"\n[STREAMING API ERROR]: {e}")
            yield "\n\n⚠️ [Error: API service failed or key is invalid. Please try again.]"
        except Exception as e:
            print(f"\n[STREAMING UNEXPECTED ERROR]: {e}")
            yield "\n\n⚠️ [Error: Connection interrupted. Please try again.]"

    return Response(stream_with_context(generate_chunks()), mimetype="text/plain")


if __name__ == "__main__":
    app.run(port=5000, debug=True)