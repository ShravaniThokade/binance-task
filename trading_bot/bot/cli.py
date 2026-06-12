import argparse
import logging
import sys

from trading_bot.bot.exceptions import ValidationError
from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import format_order_response, format_order_summary
from trading_bot.bot.service import submit_order
from trading_bot.bot.validators import validate_order_request

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place orders on Binance Futures USDT-M Demo Trading.",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        choices=["MARKET", "LIMIT"],
        help="Order type",
    )
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Limit price (required for LIMIT)")
    return parser


def main(argv: list[str] | None = None) -> int:
    setup_logging()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        request = validate_order_request(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"VALIDATION ERROR: {exc}", file=sys.stderr)
        return 1

    print(format_order_summary(request))
    logger.info(
        "Order request validated: %s %s %s qty=%s",
        request.side,
        request.order_type,
        request.symbol,
        request.quantity,
    )
    print()

    outcome = submit_order(request)

    if not outcome.success:
        if outcome.error_type == "validation":
            print(f"VALIDATION ERROR: {outcome.error_message}", file=sys.stderr)
            return 1
        if outcome.error_type == "api":
            code = f" [{outcome.error_code}]" if outcome.error_code is not None else ""
            print(f"API ERROR{code}: {outcome.error_message}", file=sys.stderr)
            return 2
        if outcome.error_type == "network":
            print(f"NETWORK ERROR: {outcome.error_message}", file=sys.stderr)
            print("Check your internet connection and try again.", file=sys.stderr)
            return 2
        print(f"ERROR: {outcome.error_message}", file=sys.stderr)
        return 2

    print(format_order_response(outcome.result))
    print()
    print("SUCCESS: Order placed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
