import logging
from dataclasses import dataclass

from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.validators import OrderRequest

logger = logging.getLogger(__name__)


def _to_decimal_str(value: float) -> str:
    """Format a float for Binance API (avoids scientific notation)."""
    text = f"{value:.8f}".rstrip("0").rstrip(".")
    return text if text else "0"


@dataclass(frozen=True)
class OrderResult:
    order_id: int
    status: str
    executed_qty: str
    avg_price: str | None
    raw_response: dict


def build_order_params(request: OrderRequest) -> dict:
    params: dict = {
        "symbol": request.symbol,
        "side": request.side,
        "type": request.order_type,
        "quantity": _to_decimal_str(request.quantity),
    }

    if request.order_type == "LIMIT":
        params["price"] = _to_decimal_str(request.price)  # type: ignore[arg-type]
        params["timeInForce"] = "GTC"

    return params


def place_order(client: BinanceFuturesClient, request: OrderRequest) -> OrderResult:
    params = build_order_params(request)
    logger.info("Submitting %s %s order for %s", request.side, request.order_type, request.symbol)
    response = client.place_order(**params)

    return OrderResult(
        order_id=response["orderId"],
        status=response.get("status", "UNKNOWN"),
        executed_qty=response.get("executedQty", "0"),
        avg_price=response.get("avgPrice") or None,
        raw_response=response,
    )


def format_order_summary(request: OrderRequest) -> str:
    lines = [
        "--- Order Request Summary ---",
        f"  Symbol   : {request.symbol}",
        f"  Side     : {request.side}",
        f"  Type     : {request.order_type}",
        f"  Quantity : {request.quantity}",
    ]
    if request.price is not None:
        lines.append(f"  Price    : {request.price}")
    return "\n".join(lines)


def format_order_response(result: OrderResult) -> str:
    avg = result.avg_price if result.avg_price and float(result.avg_price) > 0 else "N/A"
    return (
        "--- Order Response ---\n"
        f"  Order ID     : {result.order_id}\n"
        f"  Status       : {result.status}\n"
        f"  Executed Qty : {result.executed_qty}\n"
        f"  Avg Price    : {avg}"
    )
