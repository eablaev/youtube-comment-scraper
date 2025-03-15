import os
import googleapiclient.discovery
from dotenv import load_dotenv
import google.generativeai as genai
import pandas as pd

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)
channel_id = os.getenv("YOUTUBE_CHANNEL_ID")

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-pro-001")

def get_channel_videos(channel_id):
    video_ids = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,  
            order="date",
            pageToken=next_page_token  # Request the next page
        )
        response = request.execute()

        # Extract video IDs
        video_ids.extend([item["id"]["videoId"] for item in response.get("items", []) if "videoId" in item["id"]])

        # Get the nextPageToken, if it exists
        next_page_token = response.get("nextPageToken")

        # Stop if there are no more pages
        if not next_page_token:
            break

    return video_ids


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

userInput= f"Analyze the following YouTube comments and summarize key themes, sentiment, and engagement trends"  

def analyze_comments(comments, userInput):  
    prompt= f"{userInput}:\n\n{comments}"  
    response = model.generate_content(prompt)  
    return response.text 




video_ids = get_channel_videos(channel_id)

all_comments = []
for video_id in video_ids:
    print(f"Fetching comments for video: {video_id}")
    comments = get_video_comments(video_id)
    all_comments.extend(comments)

# Convert to a DataFrame and save to CSV
df = pd.DataFrame({"Comments": all_comments})
df.to_csv("youtube_comments.csv", index=False)

 
analysis = analyze_comments(all_comments,userInput)  
print(analysis) 



print("Comments saved to youtube_comments.csv")



