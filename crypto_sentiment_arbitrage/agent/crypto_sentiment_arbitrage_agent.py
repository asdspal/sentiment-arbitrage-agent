# src/agent/crypto_sentiment_arbitrage_agent.py

from hive_agent import HiveAgent
from crypto_sentiment_arbitrage.services.gdelt_service import GDELTService
from crypto_sentiment_arbitrage.services.sentiment_analysis_service import SentimentAnalysisService
from crypto_sentiment_arbitrage.services.arbitrage_service import ArbitrageService
import logging
import asyncio
import toml

logger = logging.getLogger(__name__)

class CryptoSentimentArbitrageAgent(HiveAgent):
  def __init__(self, name, functions, config_path):
      super().__init__(name, functions, config_path)
      with open(config_path, 'r') as config_file:
          self.config = toml.load(config_file)
      
      self.gdelt_service = GDELTService()
      self.sentiment_service = SentimentAnalysisService()
      self.arbitrage_service = ArbitrageService(self.config['arbitrage'])
      self.top_coins = self.config['arbitrage']['top_coins']

  async def analyze_crypto_sentiment(self):
      logger.info("Starting crypto sentiment analysis")
      news_by_coin = self.gdelt_service.fetch_crypto_news(self.top_coins)
      sentiment_scores = self.sentiment_service.analyze_news_sentiment(news_by_coin)
      
      logger.info("Sentiment analysis results:")
      for coin, score in sentiment_scores.items():
          logger.info(f"{coin}: {score}")
      
      return sentiment_scores

  async def detect_arbitrage_opportunities(self):
      logger.info("Detecting arbitrage opportunities")
      opportunities = await self.arbitrage_service.detect_arbitrage()
      
      logger.info("Arbitrage opportunities:")
      for opp in opportunities:
          logger.info(f"Pair: {opp['pair']}, Buy: {opp['buy_exchange']}, Sell: {opp['sell_exchange']}, Profit: {opp['profit_percentage']:.2f}%")
      
      return opportunities

  async def run_analysis_loop(self):
      while True:
          sentiment_scores = await self.analyze_crypto_sentiment()

          #arbitrage_opportunities = await self.detect_arbitrage_opportunities()
          
          # Combine sentiment and arbitrage data
          
          #for opp in arbitrage_opportunities:
          #    coin = opp['pair'].split('/')[0]
          #    if coin in sentiment_scores:
          #        opp['sentiment_score'] = sentiment_scores[coin]
          
          # Here you could add logic to store or act on the combined data
          
          await asyncio.sleep(600)  # Wait for 10 minutes

  async def run(self):
      await self.run_analysis_loop()


def get_crypto_sentiment_arbitrage():
  agent = CryptoSentimentArbitrageAgent("crypto_sentiment_arbitrage_agent", [], "config/config.toml")
  asyncio.run(agent.run())

if __name__ == "__main__":
  get_crypto_sentiment_arbitrage()
