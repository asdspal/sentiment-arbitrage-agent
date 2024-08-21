# Crypto Sentiment and Arbitrage Agent

This project implements an AI agent that analyzes cryptocurrency sentiment from news sources and detects cross-chain arbitrage opportunities. It uses the GDELT project for news retrieval, Together.ai for sentiment analysis, and checks multiple exchanges for arbitrage opportunities.

## Features

- Fetches and analyzes sentiment for top 20 cryptocurrencies every 10 minutes
- Detects arbitrage opportunities across multiple exchanges
- Combines sentiment data with arbitrage opportunities for comprehensive market insights

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Together.ai API key

## Installation

1. Clone the repository:

git clone https://github.com/asdspal/crypto-sentiment-arbitrage-agent.git
cd crypto-sentiment-arbitrage-agent


2. Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate


3. Install the required packages:

pip install -r requirements.txt


4. Set up your Together.ai API key as an environment variable:

export TOGETHER_API_KEY=your_api_key_here

   On Windows, use `set TOGETHER_API_KEY=your_api_key_here`

## Configuration

The project uses a YAML configuration file located at `config/config.yaml`. You can modify this file to:

- Add or remove exchanges for arbitrage detection
- Change the trading pairs to monitor
- Update the list of top cryptocurrencies for sentiment analysis

## Running the Agent

To run the agent, use the following command from the project root directory:

python src/main.py


The agent will start running and will perform sentiment analysis and arbitrage detection every 10 minutes. Results will be logged to the console.

## Project Structure

crypto-sentiment-arbitrage-agent/
│
├── src/
│   ├── agent/
│   │   ├── init.py
│   │   └── crypto_sentiment_arbitrage_agent.py
│   ├── services/
│   │   ├── init.py
│   │   ├── gdelt_service.py
│   │   ├── sentiment_analysis_service.py
│   │   └── arbitrage_service.py
│   ├── utils/
│   │   ├── init.py
│   │   └── helpers.py
│   └── main.py
│
├── tests/
│   ├── init.py
│   ├── test_gdelt_service.py
│   ├── test_sentiment_analysis_service.py
│   └── test_arbitrage_service.py
│
├── config/
│   └── config.yaml
│
├── requirements.txt
├── README.md
└── .gitignore


## Testing

To run the tests, use the following command from the project root directory:

python -m unittest discover tests


This will run all the test files in the `tests/` directory.

## Adding New Features

To add new features or modify existing ones:

1. Create or update the relevant service in the `src/services/` directory.
2. Update the `CryptoSentimentArbitrageAgent` class in `src/agent/crypto_sentiment_arbitrage_agent.py` to use the new or modified service.
3. Update the configuration in `config/config.yaml` if necessary.
4. Add appropriate tests in the `tests/` directory.

## Troubleshooting

- If you encounter issues with API rate limits, consider implementing retry logic with exponential backoff.
- For performance issues, you may need to optimize the frequency of API calls or implement caching mechanisms.
- If you're having trouble with the Together.ai API, make sure your API key is correctly set and that you have sufficient credits.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- GDELT Project for providing news data
- Together.ai for sentiment analysis capabilities
- Various cryptocurrency exchanges for price data


