# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 19:49:45 2023

@author: Indira
"""

import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import filedialog

import numpy as np
import scipy

print("NumPy version:", np.__version__)
print("SciPy version:", scipy.__version__)

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

def analyze_sentiment(text):
    # Tokenize the text
    words = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    # Combine words into a sentence
    cleaned_text = ' '.join(words)

    # Analyze sentiment using NLTK's Sentiment Intensity Analyzer
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(cleaned_text)

    # Determine sentiment label based on the compound score
    if sentiment_score['compound'] >= 0.05:
        sentiment_label = 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    return sentiment_label, sentiment_score


def company_sentiment_analysis():
    # Create a Tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog to select the CSV file
    csv_file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])

    # Check if the user selected a file
    if csv_file_path:
        # Get user input for a brand name
        brand_name = input("Enter your company's brand name: ")

        # Read tweets from CSV file
        df = pd.read_csv(csv_file_path)

        # Analyze sentiments
        positive_tweets = []
        negative_tweets = []
        neutral_tweets = []

        for tweet in df['tweet']:
            sentiment_label, _ = analyze_sentiment(tweet)
            if sentiment_label == 'Positive':
                positive_tweets.append(tweet)
            elif sentiment_label == 'Negative':
                negative_tweets.append(tweet)
            else:
                neutral_tweets.append(tweet)

        # Count the number of positive, negative, and neutral tweets
        num_positive = len(positive_tweets)
        num_negative = len(negative_tweets)
        num_neutral = len(neutral_tweets)

        print(f"\nSentiment Analysis for {brand_name}'s Tweets:")
        print(f"Number of Positive Tweets: {num_positive}")
        print(f"Number of Negative Tweets: {num_negative}")
        print(f"Number of Neutral Tweets: {num_neutral}")

        # Allow the user to print 5 positive and 5 negative tweets
        print("\nPositive Tweets:")
        for i, tweet in enumerate(positive_tweets[:5], 1):
            print(f"{i}. {tweet}")

        print("\nNegative Tweets:")
        for i, tweet in enumerate(negative_tweets[:5], 1):
            print(f"{i}. {tweet}")

        return positive_tweets, negative_tweets, neutral_tweets
    else:
        print("No file selected. Exiting.")
        return [], [], []

# Example usage
positive_tweets, negative_tweets, neutral_tweets = company_sentiment_analysis()

# User can call to print more positive or negative tweets
while True:
    user_action = input("Do you want to print more tweets? (yes/no): ").lower()
    if user_action == 'yes':
        sentiment_type = input("Enter the sentiment type (positive/negative/neutral): ").lower()
        if sentiment_type == 'positive':
            for i, tweet in enumerate(positive_tweets[5:], 1):
                print(f"{i}. {tweet}")
        elif sentiment_type == 'negative':
            for i, tweet in enumerate(negative_tweets[5:], 1):
                print(f"{i}. {tweet}")
        elif sentiment_type == 'neutral':
            for i, tweet in enumerate(neutral_tweets[5:], 1):
                print(f"{i}. {tweet}")
        else:
            print("Invalid sentiment type. Please enter 'positive', 'negative', or 'neutral'.")
    else:
        break
