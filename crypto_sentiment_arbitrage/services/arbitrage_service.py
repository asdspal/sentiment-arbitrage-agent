# src/services/arbitrage_service.py

import asyncio
import aiohttp
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ArbitrageService:
  def __init__(self, config):
      self.exchanges = config['exchanges']
      self.pairs = config['pairs']

  async def fetch_price(self, session, exchange, pair):
      url = f"{exchange['url']}/{pair}"
      try:
          async with session.get(url) as response:
              if response.status == 200:
                  data = await response.json()
                  return {
                      'exchange': exchange['name'],
                      'pair': pair,
                      'price': float(data[exchange['price_key']])
                  }
              else:
                  logger.error(f"Error fetching price from {exchange['name']} for {pair}: Status {response.status}")
                  return None
      except Exception as e:
          logger.error(f"Error fetching price from {exchange['name']} for {pair}: {e}")
          return None

  async def fetch_all_prices(self):
      async with aiohttp.ClientSession() as session:
          tasks = [
              self.fetch_price(session, exchange, pair)
              for exchange in self.exchanges
              for pair in self.pairs
          ]
          results = await asyncio.gather(*tasks)
          return [r for r in results if r is not None]

  def find_arbitrage_opportunities(self, prices):
      opportunities = []
      for pair in self.pairs:
          pair_prices = [p for p in prices if p['pair'] == pair]
          if len(pair_prices) < 2:
              continue
          
          lowest = min(pair_prices, key=lambda x: x['price'])
          highest = max(pair_prices, key=lambda x: x['price'])
          
          if lowest['exchange'] != highest['exchange']:
              profit_percentage = (highest['price'] - lowest['price']) / lowest['price'] * 100
              if profit_percentage > 1:  # Only consider opportunities with > 1% profit
                  opportunities.append({
                      'pair': pair,
                      'buy_exchange': lowest['exchange'],
                      'sell_exchange': highest['exchange'],
                      'buy_price': lowest['price'],
                      'sell_price': highest['price'],
                      'profit_percentage': profit_percentage
                  })
      
      return opportunities

  async def detect_arbitrage(self):
      prices = await self.fetch_all_prices()
      opportunities = self.find_arbitrage_opportunities(prices)
      return opportunities
