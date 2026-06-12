import re
from dataclasses import dataclass
from typing import Literal

from trading_bot.bot.exceptions import ValidationError

OrderSide = Literal["BUY", "SELL"]
OrderType = Literal["MARKET", "LIMIT"]

SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]+USDT$")
VALID_SIDES = frozenset({"BUY", "SELL"})
VALID_TYPES = frozenset({"MARKET", "LIMIT"})


@dataclass(frozen=True)
class OrderRequest:
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: float | None = None


def _parse_positive_float(value: str | float, field_name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{field_name} must be a positive number.") from exc

    if parsed <= 0:
        raise ValidationError(f"{field_name} must be greater than zero.")
    return parsed


def validate_order_request(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str | float,
    price: str | float | None = None,
) -> OrderRequest:
    if not symbol:
        raise ValidationError("symbol is required.")

    symbol = symbol.upper().strip()
    if not SYMBOL_PATTERN.match(symbol):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Expected format like BTCUSDT."
        )

    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL.")

    order_type = order_type.upper().strip()
    if order_type not in VALID_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be MARKET or LIMIT."
        )

    qty = _parse_positive_float(quantity, "quantity")

    parsed_price: float | None = None

    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("price is required for LIMIT orders.")
        parsed_price = _parse_positive_float(price, "price")

    if order_type == "MARKET" and price is not None:
        raise ValidationError("price must not be provided for MARKET orders.")

    return OrderRequest(
        symbol=symbol,
        side=side,  # type: ignore[arg-type]
        order_type=order_type,  # type: ignore[arg-type]
        quantity=qty,
        price=parsed_price,
    )
