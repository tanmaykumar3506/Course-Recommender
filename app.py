from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# Course database
course_database = {
    "programming": {
        "introductory": [
            {"name": "Python for Beginners", "duration": "8 weeks", "level": "Beginner",
             "topics": ["Basic Python", "Data Types", "Control Flow", "Functions"]},
            {"name": "JavaScript Fundamentals", "duration": "6 weeks", "level": "Beginner",
             "topics": ["Basic JS", "DOM Manipulation", "Events", "Async Programming"]}
        ],
        "intermediate": [
            {"name": "Advanced Python Development", "duration": "10 weeks", "level": "Intermediate",
             "topics": ["OOP", "Decorators", "Generators", "Testing"]},
            {"name": "Full Stack Web Development", "duration": "12 weeks", "level": "Intermediate",
             "topics": ["Frontend", "Backend", "Database", "APIs"]}
        ]
    },
    "data_science": {
        "introductory": [
            {"name": "Data Science Fundamentals", "duration": "8 weeks", "level": "Beginner",
             "topics": ["Python", "Statistics", "Data Analysis", "Visualization"]},
            {"name": "Machine Learning Basics", "duration": "10 weeks", "level": "Beginner",
             "topics": ["ML Concepts", "Scikit-learn", "Neural Networks", "Model Evaluation"]}
        ],
        "intermediate": [
            {"name": "Advanced Machine Learning", "duration": "12 weeks", "level": "Intermediate",
             "topics": ["Deep Learning", "NLP", "Computer Vision", "MLOps"]},
            {"name": "Big Data Analytics", "duration": "10 weeks", "level": "Intermediate",
             "topics": ["Hadoop", "Spark", "Data Warehousing", "ETL"]}
        ]
    },
    "design": {
        "introductory": [
            {"name": "UI/UX Design Fundamentals", "duration": "8 weeks", "level": "Beginner",
             "topics": ["Design Principles", "Wireframing", "Prototyping", "User Research"]},
            {"name": "Graphic Design Basics", "duration": "6 weeks", "level": "Beginner",
             "topics": ["Color Theory", "Typography", "Layout", "Adobe Tools"]}
        ],
        "intermediate": [
            {"name": "Advanced UI/UX Design", "duration": "10 weeks", "level": "Intermediate",
             "topics": ["Design Systems", "Accessibility", "Motion Design", "Design Thinking"]},
            {"name": "Brand Identity Design", "duration": "8 weeks", "level": "Intermediate",
             "topics": ["Brand Strategy", "Logo Design", "Visual Identity", "Brand Guidelines"]}
        ]
    }
}


# Function to filter relevant courses based on keywords
def get_relevant_courses(query):
    query = query.lower()
    relevant_courses = {}

    if any(word in query for word in ["programming", "coding", "developer", "software", "code"]):
        relevant_courses["programming"] = course_database["programming"]
    if any(word in query for word in ["data", "analytics", "machine learning", "ai", "artificial intelligence"]):
        relevant_courses["data_science"] = course_database["data_science"]
    if any(word in query for word in ["design", "ui", "ux", "graphic", "visual"]):
        relevant_courses["design"] = course_database["design"]

    return relevant_courses if relevant_courses else course_database


# API Route to handle user message and respond with course recommendation
@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message', '')

    # Get relevant courses first using keyword matching
    relevant_courses = get_relevant_courses(user_message)

    # Create dynamic prompt for Gemini API using only relevant courses
    prompt = f"""
    You are a specialized course recommendation expert.

    User Query: "{user_message}"

    Available Course Information:
    {relevant_courses}

    Please provide a detailed and friendly course recommendation.
    Mention course names, duration, level, and why they are suitable.
    Use emojis where appropriate.
    """

    try:
        response = model.generate_content(prompt)
        response_message = response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        response_message = "Sorry, I encountered an error while processing your request."

    return jsonify({'response': response_message})


# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)



from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Set API key
genai.configure(api_key="AIzaSyClMVlKIRK3zvyHQjwsPBsO29_vQ0KKvmo")

# Initialize Gemini model
model = genai.GenerativeModel("gemini-pro")

@app.route('/api/send_message', methods=['POST'])
def send_message():
    try:
        user_message = request.json.get("message")
        if not user_message:
            return jsonify({"response": "No message received"}), 400

        print("User message:", user_message)

        # Send prompt to Gemini
        response = model.generate_content(user_message)
        print("Gemini response:", response)

        # Return response
        return jsonify({"response": response.text})

    except Exception as e:
        print("Error occurred:", str(e))
        return jsonify({"response": "Sorry, I encountered an error. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True)
