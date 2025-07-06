from flask import Flask, request, jsonify
import os
from pathlib import Path
from dotenv import load_dotenv
import openai

# Load environment variables
env_path = Path(__file__).parent / "proto.env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ Missing OpenAI API key.")
openai.api_key = api_key

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_input = data.get("message", "")

    prompt = f"""
    You are a helpful Shopify store assistant.
    Limit all responses to 2–3 sentences.
    If you're unsure or the question is complex, suggest connecting the customer to a human agent.
    User asked: "{user_input}"
    """

    try:
        response = openai.chat.completions.create(  # lowercase 'chat'
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Shopify assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
