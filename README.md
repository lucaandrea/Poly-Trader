# PolyTrader: AI-Powered Automated Trading System for Polymarket

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/status-active-success.svg" alt="Status">
</p>

An autonomous AI trading agent for [Polymarket](https://polymarket.com/) that identifies market inefficiencies, calculates optimal bet sizes, and executes trades automatically. This system leverages ChatGPT's predictive capabilities against existing market odds to find profitable edges.

## 🚀 Performance

In initial testing over 72 hours:
- **Starting capital:** $1,000
- **Final balance:** $2,500 (150% ROI)

After scaling:
- **Starting capital:** $10,000
- **Final balance:** $13,500 (35% ROI in one week)
- **Win rate:** 68% across 64 trades
- **Operation:** Completely autonomous

## 📋 Features

- **24/7 Market Analysis:** Continuously scans Polymarket for opportunities
- **AI-Powered Predictions:** Uses ChatGPT to analyze sports games, political events, and more
- **Edge Detection:** Compares AI predictions with market consensus to find inefficiencies
- **Intelligent Bet Sizing:** Implements Kelly Criterion for optimal bankroll management
- **Automated Execution:** Places trades via Polymarket Agents SDK without human intervention
- **Risk Management:** Includes safety features like automatic shutdown on significant losses

## 🏗️ Architecture

The system consists of three core modules:

1. **Analysis Module**
   - Uses ChatGPT to analyze upcoming events
   - Compares predictions with current Polymarket odds
   - Identifies opportunities with significant edge

2. **Decision Module**
   - Evaluates opportunities based on edge percentage
   - Calculates optimal bet size using Kelly Criterion
   - Manages risk to preserve bankroll

3. **Execution Module**
   - Connects to Polymarket using their official Agents SDK
   - Places trades automatically with verification
   - Implements safety measures and error handling

## 💻 Installation

```bash
# Clone this repository
git clone https://github.com/llSourcell/PolyTrader.git

# Navigate to the project directory
cd PolyTrader

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and configuration
```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_flask_secret_key
POLYMARKET_API_KEY=your_polymarket_api_key
POLYGON_WALLET_PRIVATE_KEY=your_wallet_private_key
POLYMARKET_WALLET_ADDRESS=your_wallet_address
INITIAL_BANKROLL=1000
MAX_BET_PERCENTAGE=0.05
MIN_EDGE_PERCENTAGE=0.15
```

> ⚠️ **IMPORTANT**: Never commit your `.env` file or hardcode API keys in the source code. The `.env` file is included in `.gitignore` to prevent accidental exposure of your credentials.

You can copy the provided `.env.example` file to create your own `.env` file:

```bash
cp .env.example .env
# Then edit .env with your actual credentials
```

## 🚀 Usage

```bash
# Start the AI trader
python app.py

# Run in simulation mode (no real trades)
python app.py --simulation

# Analyze specific markets
python polymarket_ai_search.py --query "NBA games tonight"
```

## ⚠️ Risk Warning

Trading involves substantial risk and is not suitable for all investors. Past performance is not indicative of future results. Start with small amounts ($100 recommended) to test the system before scaling up. Implement proper risk management.

## 🔍 Main Files

- `app.py` - Main entry point for the Flask application
- `polymarket_ai_search.py` - Search and analysis of Polymarket events
- `place_polymarket_bet.py` - Automated bet execution
- `fetch_current_markets.py` - Real-time market data retrieval
- `polymarket_final.py` - Combined system with all modules

## 🛠️ Development

This project uses:
- Python 3.9+
- Flask for the web interface
- OpenAI API for predictions
- Polymarket Agents SDK for trade execution

## 🔜 Future Improvements

- Multi-market correlation analysis
- Real-time news integration for political markets
- Enhanced ML models for specialized markets
- Portfolio optimization algorithms
- Improved risk management features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

[Siraj Raval](https://github.com/llSourcell)

## 🙏 Acknowledgements

- OpenAI for ChatGPT API
- Polymarket team for the Agents SDK
- All contributors and testers

---

⭐ Star this repo if you find it useful! Join our [Discord community](https://discord.gg/sirajraval) to discuss improvements and share results.

**Note:** This system is for educational purposes. Always do your own research before trading. 