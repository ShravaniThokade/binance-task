# Binance Futures Demo Trading Bot

A small Python application that places orders on **Binance Futures USDT-M Demo Trading** with structured code, file logging, and error handling. Includes a CLI and a Streamlit web UI (bonus feature).

## Features

- Place **MARKET** and **LIMIT** orders
- Support **BUY** and **SELL** sides
- CLI input validation via `argparse`
- **Streamlit web UI** for browser-based order placement (bonus)
- Layered architecture: CLI/UI → service → validators/orders → API client
- Request/response logging to `logs/trading_bot.log`
- Exception handling for invalid input, API errors, and network failures

## Prerequisites

- Python 3.10 or newer
- A Binance account with **Demo Trading** enabled

## API Key Setup

Binance has replaced the legacy futures testnet (`testnet.binancefuture.com`) with **Demo Trading**. The old URL now redirects to the demo portal.

1. Log in at [Binance](https://www.binance.com) and open **Demo Trading** (or go to [demo.binance.com](https://demo.binance.com))
2. Open **API Key Management** inside Demo Trading and create a new key
3. Enable **Futures trading** permission on the key
4. Copy the key and secret into your `.env` file

API base URL used by this bot: `https://demo-fapi.binance.com` ([official docs](https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info))

> **Note:** Demo Trading API keys are separate from production keys and from the old testnet keys. Keys from the legacy testnet portal will not work.

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

## Usage

### CLI

Run from the project root:

```bash
python -m trading_bot.bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--symbol` | Yes | Trading pair (e.g. `BTCUSDT`) |
| `--side` | Yes | `BUY` or `SELL` |
| `--type` | Yes | `MARKET` or `LIMIT` |
| `--quantity` | Yes | Order quantity (positive number) |
| `--price` | LIMIT | Limit price |

#### Examples

**Market BUY:**

```bash
python -m trading_bot.bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Limit SELL:**

```bash
python -m trading_bot.bot.cli --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 95000
```

### Web UI (bonus)

Launch the Streamlit interface from the **project root** (`shrav/`):

```bash
streamlit run run_ui.py
```

Alternatively: `streamlit run trading_bot/bot/ui.py` (also works when run from the project root).

Open the URL shown in the terminal (typically `http://localhost:8501`). Fill in the form and click **Place Order**. The UI shows validation errors, order summary, and response details.

### Sample CLI Output

```
--- Order Request Summary ---
  Symbol   : BTCUSDT
  Side     : BUY
  Type     : MARKET
  Quantity : 0.001

--- Order Response ---
  Order ID     : 2847561093
  Status       : FILLED
  Executed Qty : 0.001
  Avg Price    : 67234.50000

SUCCESS: Order placed successfully.
```

## Project Structure

```
trading_bot/
  bot/
    cli.py              # CLI entry point (argparse)
    ui.py               # Streamlit web UI (bonus)
    service.py          # Shared order execution logic
    client.py           # Binance Futures demo client wrapper
    orders.py           # Order placement and output formatting
    validators.py       # Input validation
    logging_config.py   # File + console logging setup
    exceptions.py       # Custom exception types
logs/
  trading_bot.log       # Runtime log (created on first run)
  examples/
    market_order.log    # Example log from a MARKET order
    limit_order.log     # Example log from a LIMIT order
```

## Assumptions

- All API calls use the Binance Futures Demo URL: `https://demo-fapi.binance.com`
- **One-way position mode** (default `BOTH`); hedge mode is not supported
- LIMIT orders use `timeInForce: GTC`
- MARKET orders fill immediately; LIMIT orders may remain `NEW` until price is reached
- Minimum quantity and notional limits are enforced by Binance per symbol

## Logging

- Logs are written to `logs/trading_bot.log` (append mode)
- Console shows INFO-level messages; the log file captures DEBUG details including full API responses
- Example log excerpts are provided in `logs/examples/` for submission

## Exit Codes (CLI)

| Code | Meaning |
|------|---------|
| 0 | Order placed successfully |
| 1 | Validation error (bad input or missing credentials) |
| 2 | API or network error |

## Troubleshooting

| Error | Likely cause | Fix |
|-------|--------------|-----|
| Missing API credentials | `.env` not configured | Copy `.env.example` to `.env` and add keys |
| `-1111` Precision error | Quantity/price decimal places | Match symbol step size from exchange info |
| `-2019` Margin insufficient | Low demo balance | Reset demo wallet in Demo Trading settings |
| `-2015` Invalid API key | Wrong key type or portal | Create keys in Demo Trading, not production or legacy testnet |
| `-4164` Min notional | Order value too small | Increase quantity or price |
| Network failure | Connectivity issue | Check internet and retry |

## License

MIT (or as required by your submission).
