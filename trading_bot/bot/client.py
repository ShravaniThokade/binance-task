import logging
import os

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

from trading_bot.bot.exceptions import APIError, NetworkError, ValidationError

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    # Binance replaced the legacy futures testnet with Demo Trading.
    # See: https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info
    DEMO_URL = "https://demo-fapi.binance.com"

    def __init__(self, api_key: str | None = None, api_secret: str | None = None):
        load_dotenv()
        self._api_key = api_key or os.getenv("BINANCE_API_KEY")
        self._api_secret = api_secret or os.getenv("BINANCE_API_SECRET")

        if not self._api_key or not self._api_secret:
            raise ValidationError(
                "Missing API credentials. Set BINANCE_API_KEY and BINANCE_API_SECRET "
                "in a .env file (see .env.example)."
            )

        self._client = Client(self._api_key, self._api_secret, demo=True)
        logger.info("Binance Futures client initialized (demo: %s)", self.DEMO_URL)

    def place_order(self, **params) -> dict:
        safe_params = {k: v for k, v in params.items()}
        logger.info("Placing order: %s", safe_params)

        try:
            response = self._client.futures_create_order(**params)
        except BinanceAPIException as exc:
            logger.error("Binance API error [%s]: %s", exc.code, exc.message)
            raise APIError(exc.message, code=exc.code) from exc
        except BinanceRequestException as exc:
            logger.error("Network/request error: %s", exc)
            raise NetworkError(
                f"Network failure while contacting Binance: {exc}"
            ) from exc

        logger.debug("Order response: %s", response)
        return response
