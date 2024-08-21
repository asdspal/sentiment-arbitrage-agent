# src/services/sentiment_analysis_service.py

from together import Together
from typing import List, Dict
import os
import logging
from dotenv import load_dotenv
import json

load_dotenv("./.env")

logger = logging.getLogger(__name__)

class SentimentAnalysisService:
  def __init__(self):

      
      self.client = Together(api_key=os.getenv('TOGETHER_API_KEY'))
      self.model = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

  def analyze_sentiment(self, text: str) -> float:
      prompt = f"""Analyze the sentiment of the following text related to cryptocurrency. 
      Rate the sentiment on a scale from -1 (very negative) to 1 (very positive).
      Only respond with a number between -1 and 1.

      Text: {text}

      Sentiment score:"""
      
      
      try:
          response = self.client.completions.create(
              prompt=prompt,
              model=self.model,
              max_tokens=10,
              temperature=0.1
          )
          print(response.choices[0].text)
          sentiment_score = float(response.choices[0].text.strip())
          return max(-1, min(1, sentiment_score))  # Ensure the score is between -1 and 1
      except Exception as e:
          logger.error(f"Error in sentiment analysis: {e}")
          return 0  # Neutral sentiment in case of error
          

  def analyze_news_sentiment(self, news_by_coin: Dict[str, List[Dict]]) -> Dict[str, float]:
      sentiment_scores = {}
      for coin, news_list in news_by_coin.items():
          if not news_list:
              sentiment_scores[coin] = 0
              continue
          
          total_sentiment = 0
          #only use top 5 news articles 
          for news in news_list[0:5]:
              title_sentiment = self.analyze_sentiment(news['title'])
              total_sentiment += title_sentiment
          
          average_sentiment = total_sentiment / len(news_list)
          sentiment_scores[coin] = average_sentiment
      
      return sentiment_scores
