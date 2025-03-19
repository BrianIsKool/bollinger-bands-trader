# Arbitrage Trading System using Binance and Gate.io

This project is an arbitrage trading system that uses real-time price and trade data from Binance via WebSocket and calculates statistical indicators such as Bollinger Bands (SMA and standard deviation) to determine buy and sell signals.

## Overview

The system collects data from Binance (BTC/USDT pair) in real-time, processes the data to calculate Bollinger Bands (Upper, Lower, and Middle bands), and makes buy/sell decisions based on the current price's position relative to these bands.

## Requirements

1. **Python 3.8+**
2. **Required Python packages:**
   - `asyncpg` - PostgreSQL connection library.
   - `binance` - The official Binance API library.
   - `asyncio` - Python's standard library for asynchronous programming.
   - `statistics` - For performing statistical calculations like mean and standard deviation.

3. **PostgreSQL** - A database to store historical market data.

4. **Binance API Key and Secret** - You need your Binance credentials to interact with the Binance API.

5. **Gate.io API Key and Secret** - If you are also interacting with Gate.io for arbitrage opportunities, you will need Gate.io credentials.

## Setup

### 1. Install Dependencies

To install the required libraries, run the following command:

```bash
pip install asyncpg binance
