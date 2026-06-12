import logging
from dataclasses import dataclass

from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.exceptions import APIError, NetworkError, TradingBotError, ValidationError
from trading_bot.bot.orders import OrderResult, place_order
from trading_bot.bot.validators import OrderRequest

logger = logging.getLogger(__name__)


@dataclass
class OrderOutcome:
    success: bool
    request: OrderRequest | None = None
    result: OrderResult | None = None
    error_message: str | None = None
    error_code: int | None = None
    error_type: str | None = None


def submit_order(request: OrderRequest) -> OrderOutcome:
    try:
        client = BinanceFuturesClient()
        result = place_order(client, request)
        logger.info(
            "Order placed successfully: orderId=%s status=%s executedQty=%s avgPrice=%s",
            result.order_id,
            result.status,
            result.executed_qty,
            result.avg_price or "N/A",
        )
        return OrderOutcome(success=True, request=request, result=result)
    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        return OrderOutcome(
            success=False,
            request=request,
            error_message=str(exc),
            error_type="validation",
        )
    except APIError as exc:
        logger.error("API error [%s]: %s", exc.code, exc)
        return OrderOutcome(
            success=False,
            request=request,
            error_message=str(exc),
            error_code=exc.code,
            error_type="api",
        )
    except NetworkError as exc:
        logger.error("Network error: %s", exc)
        return OrderOutcome(
            success=False,
            request=request,
            error_message=str(exc),
            error_type="network",
        )
    except TradingBotError as exc:
        logger.error("Trading bot error: %s", exc)
        return OrderOutcome(
            success=False,
            request=request,
            error_message=str(exc),
            error_type="general",
        )
