import os
import googleapiclient.discovery
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
