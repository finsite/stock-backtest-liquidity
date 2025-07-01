"""
Processor module for stock-backtest-liquidity signal generation.

Validates input messages and computes a liquidity score to assess
executability and trading risk.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import ValidatedMessage
from app.utils.validate_data import validate_message_schema

logger = setup_logger(__name__)


def validate_input_message(message: dict[str, Any]) -> ValidatedMessage:
    """
    Validate the incoming raw message against the expected schema.

    Args:
        message (dict[str, Any]): Raw input message.

    Returns:
        ValidatedMessage: A validated message object.

    Raises:
        ValueError: If the input format is invalid.
    """
    logger.debug("🔍 Validating message schema...")
    if not validate_message_schema(message):
        logger.error("❌ Invalid message schema: %s", message)
        raise ValueError("Invalid message format")
    return message  # type: ignore[return-value]


def compute_liquidity_signal(message: ValidatedMessage) -> dict[str, Any]:
    """
    Compute a liquidity score and signal based on volume and turnover.

    Args:
        message (ValidatedMessage): The validated input data.

    Returns:
        dict[str, Any]: Message enriched with liquidity score and signal.
    """
    symbol = message.get("symbol", "UNKNOWN")
    avg_volume = int(message.get("avg_volume", 1_000_000))
    turnover_ratio = float(message.get("turnover_ratio", 0.8))

    logger.info("💧 Computing liquidity signal for %s", symbol)

    # Simple scoring: higher volume and turnover = better liquidity
    score = (avg_volume / 1_000_000) + turnover_ratio
    signal = "LIQUID" if score >= 2 else "ILLIQUID"

    result = {
        "liquidity_score": round(score, 4),
        "liquidity_signal": signal,
    }

    logger.debug("✅ Liquidity result for %s: %s", symbol, result)
    return {**message, **result}
