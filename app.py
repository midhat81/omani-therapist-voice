from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Crisis keyword list (Omani Arabic)
CRISIS_KEYWORDS = ["انتحار", "موت", "أذى", "قتل", "أريد أن أموت"]

# Home route for testing
@app.route("/")
def home():
    return "✅ Omani Therapist Voice API is running. Use POST /process to interact."

# POST route for chatbot interaction
@app.route("/process", methods=["POST"])
def process_input():
    data = request.get_json()
    user_text = data.get("message", "")

    # Crisis keyword detection
    if any(word in user_text for word in CRISIS_KEYWORDS):
        return jsonify({
            "crisis": True,
            "response": "أفهم أنك تمر بوقت صعب. هل تريد التواصل مع أخصائي؟ رقم الطوارئ: 999"
        })

    try:
        # GPT-4o response generation
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "أنت معالج نفسي عماني تتحدث باللهجة العمانية، وتفهم الثقافة المحلية والدين."},
                {"role": "user", "content": user_text}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        print("OpenAI API Error:", e)
        reply = "أواجه مشكلة في الرد حالياً، هل يمكنك إعادة المحاولة لاحقاً؟"

    return jsonify({
        "crisis": False,
        "response": reply
    })

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
