import googleapiclient.discovery
from googleapiclient.errors import HttpError

class YouTubeAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    def get_channel_videos(self, channel_id: str) -> list:
        """Fetch all video IDs from a channel."""
        video_ids = []
        next_page_token = None

        while True:
            request = self.youtube.search().list(
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

    def get_video_comments(self, video_id: str) -> list:
        """Fetch comments from a video."""
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100
            )
            response = request.execute()
            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(comment)
        except HttpError as e:
            print(f"Error fetching comments for video {video_id}: {e}")
        return comments