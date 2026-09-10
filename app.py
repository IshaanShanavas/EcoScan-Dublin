import base64
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

class DublinRecyclingRule(BaseModel): #project idea schema for structured JSON response
    item_name: str
    item_category: str
    bin_type: str  # E.G. "GREEN BIN (RECYCLING)", "BROWN BIN (COMPOST)", "BLACK BIN (GENERAL)", "CIVIC AMENITY / BRING BANK"
    disposal_steps: list[str]
    dublin_local_tip: str


# 2. CREATE MULTIMODAL API ROUTE
@app.route("/api/ecoscan", methods=["POST"])
def ecoscan():
    data = request.get_json() or {}
    image_b64 = data.get("image", "")

    if not image_b64:
        return jsonify({"status": "error", "message": "NO IMAGE PROVIDED. PLEASE UPLOAD AN IMAGE."}), 400

    try:
        # EXTRACT MIME TYPE AND DECODE BASE64 IMAGE BYTES
        if "," in image_b64:
            header, image_b64_data = image_b64.split(",", 1)
            mime_type = header.split(";")[0].split(":")[1]
        else:
            header = ""
            image_b64_data = image_b64
            mime_type = "image/jpeg"

        image_bytes = base64.b64decode(image_b64_data)
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

        prompt = (
            "ANALYZE THIS HOUSEHOLD ITEM. IDENTIFY WHAT IT IS AND PROVIDE OFFICIAL "
            "WASTE DISPOSAL AND RECYCLING RULES ACCORDING TO DUBLIN CITY COUNCIL AND MYWASTE.IE GUIDELINES." \
            "RETURN THE RESPONSE IN STRUCTURED JSON FORMAT WITH THE FOLLOWING FIELDS: " \
            "item_name, item_category, bin_type, disposal_steps, dublin_local_tip." \
            "ALSO PROVIDE A BRIEF EXPLANATION OF WHY THIS ITEM BELONGS IN THE SPECIFIED BIN TYPE."
            "ALSO AN EMOJI COLOR OF THE BIN COLOR (GREEN, BROWN, BLACK) SHOULD BE INCLUDED IN THE RESPONSE."
        )

   
        response = client.models.generate_content(
            model=MODEL,
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=DublinRecyclingRule,
                temperature=0.1,
            ),
        )

        parsed_data = json.loads(response.text)
        return jsonify({"status": "success", "data": parsed_data})

    except APIError as e:
        print(f"[GEMINI API ERROR]: {e}")
        return jsonify({"status": "error", "message": "GEMINI API FAILURE OR RATE LIMIT EXCEEDED."}), 502

    except json.JSONDecodeError:
        print("[PARSE ERROR]: INVALID JSON RETURNED FROM MODEL.")
        return jsonify({"status": "error", "message": "FAILED TO PARSE STRUCTURED RECYCLING DATA."}), 500

    except Exception as e:
        print(f"[SERVER ERROR]: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)