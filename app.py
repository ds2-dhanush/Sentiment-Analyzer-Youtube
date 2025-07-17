
import os
import re
from collections import Counter

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from googleapiclient.discovery import build
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are present
after_download = False
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    after_download = True

# ---------------------------------------------------------------------
# 🛠 Helpers
# ---------------------------------------------------------------------

def get_api_client(api_key: str):
    """Return a YouTube API client"""
    return build('youtube', 'v3', developerKey=api_key, cache_discovery=False)


def extract_video_id(url: str) -> str | None:
    """Extract 11‑char YouTube video ID from any URL format."""
    pattern = r"(?:v=|/)([0-9A-Za-z_-]{11}).*"
    m = re.search(pattern, url)
    return m.group(1) if m else None


def fetch_comments(video_id: str, api_key: str, max_comments: int = 200) -> pd.DataFrame:
    """Fetch top‑level comments up to max_comments"""
    service = get_api_client(api_key)
    comments: list[str] = []
    next_token = None

    while len(comments) < max_comments:
        request = service.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(100, max_comments - len(comments)),
            pageToken=next_token,
            textFormat="plainText",
        )
        response = request.execute()

        comments.extend([
            item['snippet']['topLevelComment']['snippet']['textDisplay']
            for item in response.get('items', [])
        ])
        next_token = response.get('nextPageToken')
        if not next_token:
            break
    return pd.DataFrame({'Comment': comments})


# ---------------------------------------------------------------------
# 🧹 Text cleaning & sentiment
# ---------------------------------------------------------------------

def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)            # remove URLs
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text)   # special chars
    return text.lower().strip()


def classify_sentiment(text: str) -> str:
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.05:
        return "Positive"
    elif polarity < -0.05:
        return "Negative"
    return "Neutral"


def top_keywords(df: pd.DataFrame, sentiment: str, n: int = 15):
    words = " ".join(df[df['Sentiment'] == sentiment]['Cleaned']).split()
    meaningful = [w for w in words if w not in stop_words and len(w) > 2]
    return Counter(meaningful).most_common(n)

# ---------------------------------------------------------------------
# 🎨 Streamlit UI
# ---------------------------------------------------------------------

st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="wide")

st.title("📺 Social‑Buzz Sentiment Analyzer")
st.markdown("Paste any *YouTube video URL*, choose how many comments to analyse, and see the crowd's mood in seconds.")

with st.sidebar:
    st.sidebar.info("🔓 Default demo key will be used unless you provide your own. For heavy use, use your own key.")
    st.header("🔑 API Key & Settings")
    use_own = st.checkbox("🔐 Use my own API key")
    if use_own:
        api_key = st.text_input("Enter your YouTube API Key", type="password")
    else:
        # 👇restricted API key
        api_key = "AIzaSyDxO80tz2nhBLOoGC5PmBCJ5aSeRQOMIFM"

    max_comments = st.slider("Number of comments", 50, 1000, 200, 50)

video_url = st.text_input("🎞️ YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Analyze Sentiment"):
    if not (api_key and video_url):
        st.error("⚠️ Enter both an API key and a YouTube video URL.")
    else:
        vid = extract_video_id(video_url)
        if not vid:
            st.error("Invalid YouTube URL. Could not extract video ID.")
        else:
            with st.spinner("Fetching comments …"):
                df = fetch_comments(vid, api_key, max_comments)
            st.write(f"Fetched *{len(df)}* comments.")

            # Clean & sentiment
            df['Cleaned'] = df['Comment'].apply(clean_text)
            df['Sentiment'] = df['Cleaned'].apply(classify_sentiment)

            # Display sentiment distribution
            st.subheader("📊 Sentiment Distribution")
            sentiment_counts = df['Sentiment'].value_counts()
            fig1, ax1 = plt.subplots()
            ax1.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=90, colors=["#7DD97B", "#FF6961", "#FFD966"])
            ax1.axis('equal')
            st.pyplot(fig1)

            st.markdown("---")
            col_pos, col_neg = st.columns(2)

            # Positive wordcloud
            with col_pos:
                st.subheader("Top Positive Keywords")
                pos_words = top_keywords(df, 'Positive', 50)
                if pos_words:
                    wc_pos = WordCloud(width=400, height=300, background_color='white').generate_from_frequencies(dict(pos_words))
                    st.image(wc_pos.to_array())
                else:
                    st.info("No positive words found.")

            # Negative wordcloud
            with col_neg:
                st.subheader("Top Negative Keywords")
                neg_words = top_keywords(df, 'Negative', 50)
                if neg_words:
                    wc_neg = WordCloud(width=400, height=300, background_color='white', colormap='Reds').generate_from_frequencies(dict(neg_words))
                    st.image(wc_neg.to_array())
                else:
                    st.info("No negative words found.")

            st.markdown("---")
            st.subheader("💬 Comment Table (with Sentiment)")
            st.dataframe(df[['Comment', 'Sentiment']])

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download CSV", csv, "youtube_sentiment_results.csv", "text/csv")

            st.success("Analysis complete!")
