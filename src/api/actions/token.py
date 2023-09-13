import random
import string

import boto3

from settings import localstack_endpoint_url


def generate_reset_password_token(length: int = 32):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def send_reset_token(email: str, reset_token):
    ses_client = boto3.client(
        "ses",
        region_name="us-east-1",
        endpoint_url=localstack_endpoint_url,
    )

    subject = "Reset Password"
    body = f"Password reset link: http://localhost:8000/auth/reset-password?token={reset_token}"

    response = ses_client.send_email(
        Source="sender@example.com",
        Destination={"ToAddresses": [email]},
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
    )
    return response


def store_reset_token(redis, email, token):
    redis.set(email, token)


def get_reset_token(redis, email):
    return redis.get(email).decode("utf-8")
