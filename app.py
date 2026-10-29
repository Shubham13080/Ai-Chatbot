import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="public", static_url_path="")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

CATEGORY_PROMPTS = {
    "IT": (
        "You are a helpful IT assistant. Answer questions about computers, software, "
        "web development, programming, networking, cybersecurity, and technology. "
        "Explain in simple language and use examples when helpful."
    ),
    "Medical": (
        "You provide general health information only, not a diagnosis. Be careful, "
        "encourage consulting a qualified healthcare professional for personal medical "
        "decisions, and advise urgent medical care for emergency symptoms."
    ),
    "ShareMarket": (
        "You are an educational stock-market assistant. Explain market concepts, "
        "indices, investing, and financial terms clearly. Do not promise returns or "
        "present personalized financial advice. Mention that markets involve risk."
    ),
}

def classify_question(message):
    """Choose a category using simple keyword matching."""
    text = message.lower()

    medical_words = [
        "fever", "pain", "doctor", "medicine", "medical", "health", "symptom",
        "headache", "cough", "cold", "hospital", "दर्द", "बुखार", "दवा", "डॉक्टर",
    ]
    market_words = [
        "share", "stock", "market", "nifty", "sensex", "investment", "invest",
        "trading", "ipo", "mutual fund", "शेयर", "निफ्टी", "सेंसेक्स", "बाजार",
    ]

    if any(word in text for word in medical_words):
        return "Medical"
    if any(word in text for word in market_words):
        return "ShareMarket"
    return "IT"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or request.form
    message = (data.get("message") or "").strip()
    category = (data.get("category") or "Auto").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    if not GROQ_API_KEY:
        return jsonify({
            "error": "GROQ_API_KEY is not configured. Add it to your local .env file or Vercel Environment Variables."
        }), 500

    if category == "Auto" or category not in CATEGORY_PROMPTS:
        category = classify_question(message)

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": CATEGORY_PROMPTS[category]},
            {"role": "user", "content": message},
        ],
        "temperature": 0.5,
        "max_tokens": 900,
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            GROQ_API_URL, headers=headers, json=payload, timeout=45
        )
        response.raise_for_status()
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        return jsonify({"answer": answer, "category": category})
    except requests.exceptions.Timeout:
        return jsonify({"error": "The AI service took too long. Please try again."}), 504
    except requests.exceptions.RequestException as exc:
        details = ""
        if getattr(exc, "response", None) is not None:
            try:
                details = exc.response.json().get("error", {}).get("message", "")
            except ValueError:
                details = exc.response.text[:300]
        return jsonify({"error": details or "Could not connect to the AI service. Check your API key and try again."}), 502
    except (KeyError, IndexError, TypeError):
        return jsonify({"error": "The AI service returned an unexpected response."}), 502


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
