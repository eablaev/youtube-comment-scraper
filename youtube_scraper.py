import os
import googleapiclient.discovery
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)



channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
print (channel_id )

def get_channel_videos(channel_id):
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,  # Fetches up to 50 videos (API limit per request)
        order="date"  # Gets the most recent videos first
    )
    response = request.execute()

    video_ids = [item["id"]["videoId"] for item in response["items"] if "videoId" in item["id"]]
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




video_ids = get_channel_videos(channel_id)

all_comments = []
for video_id in video_ids:
    print(f"Fetching comments for video: {video_id}")
    comments = get_video_comments(video_id)
    all_comments.extend(comments)

# Convert to a DataFrame and save to CSV
df = pd.DataFrame({"Comments": all_comments})
df.to_csv("youtube_comments.csv", index=False)

print("Comments saved to youtube_comments.csv")



