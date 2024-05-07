from flask import Flask, request, jsonify, render_template
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Access the API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/generate_content", methods=["POST"])
def generate_content():
    data = request.get_json()

    # Validate input parameters (consider adding more as needed)
    if not data or not data.get("format") or not data.get("topic"):
        return jsonify({"error": "Missing required parameters: format and topic"}), 400

    format = data.get("format")
    topic = data.get("topic")
    emotion = data.get("emotion", "informative")  # Default emotion
    length = int(data.get("length"))  # Default length in words
    print(length)
    # Define instruction template with placeholders
    instruction_template = """Write a {emotion} {format} about {topic} in a captivating and engaging style, generate {length} words. Ensure it adheres to marketing best practices and avoid any promotional claims. add emoji's in middle as per answer"""

    # Generate content using OpenAI
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=instruction_template.format(emotion=emotion, format=format, topic=topic, length=length),
        max_tokens=100,  # Adjust max_tokens as needed for longer content
        n=1,
        stop=None,
        temperature=0.7,  # Adjust temperature for creativity vs. informativeness
    )

    # Extract generated text and return response
    generated_text = response.choices[0].text.strip()
    return jsonify({"text": generated_text})

if __name__ == "__main__":
    app.run(debug=True)
