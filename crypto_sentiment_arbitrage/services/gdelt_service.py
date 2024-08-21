# src/services/gdelt_service.py

import requests
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class GDELTService:
  BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"

  def fetch_news(self, query: str, limit: int = 10) -> List[Dict]:
      params = {
          "query": query,
          "mode": "artlist",
          "format": "json",
          "maxrecords": limit
      }
      try:
          response = requests.get(self.BASE_URL, params=params)
          response.raise_for_status()
          data = response.json()
          return data.get("articles", [])
      except requests.RequestException as e:
          logger.error(f"Error fetching news from GDELT: {e}")
          return []

  def fetch_crypto_news(self, top_coins: List[str], limit: int = 10) -> Dict[str, List[Dict]]:
      news_by_coin = {}
      for coin in top_coins:
          news_by_coin[coin] = self.fetch_news(f"{coin} cryptocurrency", limit)
      return news_by_coin
