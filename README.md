# Binance Futures Demo Trading Bot

A small Python application that places orders on **Binance Futures USDT-M Demo Trading** with structured code, file logging, and error handling.

## Features

- Place **MARKET** and **LIMIT** orders
- Support **BUY** and **SELL** sides
- CLI input validation via `argparse`
- Layered architecture: CLI → service → validators/orders → API client
- Request/response logging to `logs/trading_bot.log`
- Exception handling for invalid input, API errors, and network failures

## Prerequisites

- Python 3.10 or newer
- A Binance account with **Demo Trading** enabled

## API Key Setup

1. Log in at [Binance](https://www.binance.com) and open **Demo Trading** (or go to [demo.binance.com](https://demo.binance.com))
2. Open **API Key Management** inside Demo Trading and create a new key
3. Enable **Futures trading** permission on the key
4. Copy the key and secret into your `.env` file

API base URL: `https://demo-fapi.binance.com`

## Installation

```bash
git clone <your-repo-url>
cd shrav
pip install -r requirements.txt
```

Copy the environment template and add your demo credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
BINANCE_API_KEY=your_demo_api_key_here
BINANCE_API_SECRET=your_demo_api_secret_here
```
