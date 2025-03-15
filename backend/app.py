from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.services.youtube import YouTubeAPI
from backend.services.gemini import GeminiAI
from backend.utils.csv_handler import save_comments_to_csv
from backend.config import YOUTUBE_API_KEY, GEMINI_API_KEY, YOUTUBE_CHANNEL_ID

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
youtube_api = YouTubeAPI(YOUTUBE_API_KEY)
gemini_ai = GeminiAI(GEMINI_API_KEY)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Get video IDs and comments
        video_ids = youtube_api.get_channel_videos(YOUTUBE_CHANNEL_ID)
        all_comments = []
        for video_id in video_ids:
            comments = youtube_api.get_video_comments(video_id)
            all_comments.extend(comments)

        # Save comments to CSV
        save_comments_to_csv(all_comments)

        # Get user input from request body
        user_input = request.json.get("userInput", "Analyze the following YouTube comments")

        # Analyze comments using Gemini AI
        analysis = gemini_ai.analyze_comments(all_comments, user_input)

        # Return JSON response
        return jsonify({"analysis": analysis, "comments": all_comments})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run Flask server
if __name__ == '__main__':
    app.run(debug=True)