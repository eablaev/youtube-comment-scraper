import os
import googleapiclient.discovery
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd
from flask import Flask, request, jsonify  # Added Flask to create API
from flask_cors import CORS  # Added CORS to allow frontend-backend communication

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
channel_id = os.getenv("YOUTUBE_CHANNEL_ID")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro-001")

# Initialize Flask app
app = Flask(__name__)  
CORS(app)  # Enable Cross-Origin Resource Sharing (allows frontend to access backend)

# Function to get video IDs
def get_channel_videos(channel_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,  
            order="date",
            pageToken=next_page_token
        )
        response = request.execute()
        video_ids.extend([item["id"]["videoId"] for item in response.get("items", []) if "videoId" in item["id"]])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

# Function to get comments from a video
def get_video_comments(video_id):
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100
        )
        response = request.execute()
        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except googleapiclient.errors.HttpError as e:
        print(f"Error fetching comments for video {video_id}: {e}")
    return comments

# Function to analyze comments using Gemini AI
def analyze_comments(comments, user_input):  
    prompt = f"{user_input}:\n\n{comments}"  
    response = model.generate_content(prompt)  
    return response.text  

# Flask API route to analyze comments
@app.route('/analyze', methods=['POST'])  # Added API endpoint
def analyze():
    try:
        video_ids = get_channel_videos(channel_id)  # Get video IDs
        all_comments = []
        for video_id in video_ids:
            comments = get_video_comments(video_id)  # Fetch comments
            all_comments.extend(comments)

        # Save comments to CSV
        df = pd.DataFrame({"Comments": all_comments})
        df.to_csv("youtube_comments.csv", index=False)

        # Get user input from request body
        user_input = request.json.get("userInput", "Analyze the following YouTube comments")

        # Analyze comments using Gemini AI
        analysis = analyze_comments(all_comments, user_input)

        # Return JSON response to frontend
        return jsonify({"analysis": analysis, "comments": all_comments})  
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error if something goes wrong

# Run Flask server
if __name__ == '__main__':
    app.run(debug=True)  # Start API server
