import sys
from pathlib import Path

# Streamlit runs this file as a script; ensure the project root is importable.
_project_root = Path(__file__).resolve().parents[2]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import streamlit as st

from trading_bot.bot.exceptions import ValidationError
from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import format_order_response, format_order_summary
from trading_bot.bot.service import submit_order
from trading_bot.bot.validators import validate_order_request

setup_logging()

st.set_page_config(page_title="Binance Futures Demo Bot", layout="centered")

st.title("Binance Futures Demo Trading Bot")
st.caption("Place MARKET and LIMIT orders on Binance Futures Demo Trading (USDT-M)")

with st.form("order_form"):
    symbol = st.text_input("Symbol", value="BTCUSDT", help="e.g. BTCUSDT, ETHUSDT")
    side = st.selectbox("Side", ["BUY", "SELL"])
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
    quantity = st.number_input(
        "Quantity",
        min_value=0.001,
        value=0.001,
        step=0.001,
        format="%.3f",
        help="Minimum 0.001 for BTCUSDT (check symbol lot size on Binance).",
    )

    price = None
    if order_type == "LIMIT":
        price = st.number_input(
            "Limit Price",
            min_value=0.01,
            value=90000.0,
            step=0.01,
            format="%.2f",
        )

    submitted = st.form_submit_button("Place Order", type="primary")

if submitted:
    if quantity <= 0:
        st.error("Quantity must be greater than zero (e.g. 0.001 for BTCUSDT).")
    elif order_type == "LIMIT" and (price is None or price <= 0):
        st.error("Limit price must be greater than zero.")
    else:
        try:
            request = validate_order_request(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
            )
        except ValidationError as exc:
            st.error(f"Validation error: {exc}")
        else:
            st.subheader("Order Request")
            st.code(format_order_summary(request))

            with st.spinner("Placing order..."):
                outcome = submit_order(request)

            if not outcome.success:
                if outcome.error_type == "api" and outcome.error_code is not None:
                    st.error(f"API error [{outcome.error_code}]: {outcome.error_message}")
                elif outcome.error_type == "network":
                    st.error(f"Network error: {outcome.error_message}")
                    st.info("Check your internet connection and try again.")
                else:
                    st.error(outcome.error_message or "Order failed.")
            else:
                st.success("Order placed successfully.")
                st.subheader("Order Response")
                st.code(format_order_response(outcome.result))
                st.json(
                    {
                        "orderId": outcome.result.order_id,
                        "status": outcome.result.status,
                        "executedQty": outcome.result.executed_qty,
                        "avgPrice": outcome.result.avg_price or "N/A",
                    }
                )
