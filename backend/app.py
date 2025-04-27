from flask import Flask, request, jsonify
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import pathlib
from flask_cors import CORS

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

file_path = pathlib.Path("../knowledge_base_docs/MAHE University Guide.pdf")
file = client.files.upload(
    file=file_path
)

SYSTEM_PROMPT = """
You are a helpful AI assistant for MAHE, Dubai (Manipal Academy of Higher Education), operating on a public kiosk for prospective students and parents.
Your primary goal is to answer questions accurately and concisely based ONLY on the information you have access to or the conversation history.
Present information directly. Act as if this information is your own internal knowledge.
**Crucially: Do NOT mention that you are referencing a document, file, or any external source. Avoid phrases like "According to the document...", "The provided document states...", "Based on the file...", "Refer to page X...", etc.**
If the necessary information isn't available to you, state clearly that you don't have that specific information.
Your scope is strictly limited to MAHE's:
- Admission procedures, requirements, and deadlines.
- Academic programs, courses, and departments.
- Tuition fees, scholarships, and financial aid information provided.
- Campus facilities, building locations, and campus maps/directions based on provided info.
- Student services (like housing, library, health services) based on provided info.
- Contact information for departments or services based on provided info.
- Information related to professors and faculty.
Politely refuse requests outside this scope (like coding, jokes, general knowledge, other universities). Be professional and concise.
"""

MODEL = "gemini-1.5-flash"

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "localhost"}})

@app.route("/")
def hello():
    return "MIA is up and running!"

@app.route("/send-prompt", methods=["POST"])
def send_prompt():
    try:
        data = request.get_json()
        query = data.get("query")

        if not query:
            return jsonify({"error": "No query provided"}), 400

        # response = client.models.generate_content(
        #     model=MODEL,
        #     config=types.GenerateContentConfig(
        #         system_instruction=SYSTEM_PROMPT
        #     ),
        #     contents=[
        #         types.Part.from_bytes(
        #             data=file_path.read_bytes(),
        #             mime_type='application/pdf',
        #         ),
        #         query
        #     ]
        # )
        response = client.models.generate_content(
            model=MODEL,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
            contents=[
                file,
                query
            ]
        )

        return jsonify({"response": response.text})
    except Exception as e:
        print(f"ERROR in chat_handler: {e}")
        return jsonify({
            "response": "Something went wrong. Please try again later.",
            "error": "Internal server error"
        }), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)