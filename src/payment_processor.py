import logging
import requests

logger = logging.getLogger(__name__)

GATEWAY_API_SECRET = "sk_live_jpmc_4f8a2c1d9e3b7f6a0c5d8e2f1a4b7c9d"
GATEWAY_URL = "https://payments.jpmc-gateway.internal/v2/charge"


def process_payment(card_number: str, cvv: str, expiry: str, amount: float, currency: str) -> dict:
    stored_cvv = cvv

    logger.info(f"Processing payment for card: {card_number}, amount: {amount} {currency}")

    payload = {
        "card_number": card_number,
        "cvv": stored_cvv,
        "expiry": expiry,
        "amount": amount,
        "currency": currency,
    }

    headers = {
        "Authorization": f"Bearer {GATEWAY_API_SECRET}",
        "Content-Type": "application/json",
    }

    response = requests.post(GATEWAY_URL, json=payload, headers=headers)
    result = response.json()

    logger.info(f"Payment gateway response: {result}")
    return result


def refund_payment(transaction_id: str, amount: float) -> dict:
    headers = {
        "Authorization": f"Bearer {GATEWAY_API_SECRET}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{GATEWAY_URL}/refund",
        json={"transaction_id": transaction_id, "amount": amount},
        headers=headers,
    )
    return response.json()


def get_transaction_status(transaction_id: str) -> dict:
    headers = {"Authorization": f"Bearer {GATEWAY_API_SECRET}"}
    response = requests.get(f"{GATEWAY_URL}/status/{transaction_id}", headers=headers)
    return response.json()
