
📺 SOCIAL-BUZZ SENTIMENT ANALYZER

🧠 What is this project?
--------------------------
The Social-Buzz Sentiment Analyzer is a real-time sentiment analysis tool built using Natural Language Processing (NLP) that allows users to analyze public opinion from YouTube video comments.

Users simply enter:
1. Their own YouTube API Key (or use the provided one below),
2. A YouTube video URL,
3. Number of comments to fetch.

Then, the app processes and analyzes those comments to reveal the general sentiment (Positive / Negative / Neutral) using the TextBlob library.

✅ Why is it useful?
--------------------------
• Track public opinion during news events, movies, product launches, political content, etc.
• Understand audience mood instantly from real-world comments.
• Useful for journalists, marketers, analysts, and researchers to gather real-time social feedback.

⚙️ How does it work?
--------------------------
1. Uses the YouTube Data API to fetch comments from a video.
2. Cleans and processes the text.
3. Uses `TextBlob` for sentiment classification (positive, negative, neutral).
4. Visualizes the result using charts (pie chart + bar chart).
5. Displays top keywords for each sentiment category.

📦 Technologies Used:
--------------------------
- Python
- Streamlit (for UI)
- TextBlob (for sentiment analysis)
- NLTK (for stopwords)
- WordCloud & Matplotlib (for visualization)
- Google API Client (for YouTube comments)
- Pandas, NumPy

🔐 Your API Key (For Testing)
--------------------------
Use this key in the left sidebar of the app:

👉 API KEY:  
AIzaSyDx08tz2nhBLO0GCSPmBCJ5aSeRQ0MlFM

📌 Paste it in the “YouTube API Key” section on the left sidebar of the app.

📌 If this key fails due to limit, generate your own from:
https://console.cloud.google.com/apis

🛠 How to Run
--------------------------
1. Clone/download the project.
2. Install the required packages:
   pip install -r requirements.txt
3. Run the app:
   streamlit run app.py

📁 Folder Structure:
--------------------------
- app.py → Main Streamlit application
- .streamlit/secrets.toml (optional if you want to use secret storage)
- README.txt → You’re reading it!
- requirements.txt → Python dependencies

🎯 Example Use-Case:
--------------------------
Analyzing a YouTube video about “Iran-Israel conflict” can help quickly understand whether the public supports peace, war, or is emotionally neutral — just by analyzing comment tone.

📢 NOTE:
--------------------------
Due to Google API limitations, you can fetch up to ~1000 comments max in a single call. Use wisely!

----

© 2025 DHANUSH R. All rights reserved.
