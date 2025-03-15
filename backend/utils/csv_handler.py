import pandas as pd

def save_comments_to_csv(comments: list, filename: str = "youtube_comments.csv"):
    """Save comments to a CSV file."""
    df = pd.DataFrame({"Comments": comments})
    df.to_csv(filename, index=False)