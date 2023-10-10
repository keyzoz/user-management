import random
import string

import boto3

from settings import AWS_EMAIL_SENDER, LOCALSTACK_ENDPOINT_URL
from src.db.redis_db import get_redis_client


class ResetTokenService:
    def __init__(self):
        self.storage = None

    @property
    def redis_storage(self):
        if self.storage is None:
            self.storage = get_redis_client()
        return self.storage

    @redis_storage.setter
    def redis_storage(self, value):
        self.storage = value

    @staticmethod
    def generate_reset_password_token(length: int = 32):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def send_reset_token(email: str, reset_token):
        ses_client = boto3.client(
            "ses",
            region_name="us-east-1",
            endpoint_url=LOCALSTACK_ENDPOINT_URL,
        )

        subject = "Reset Password"
        body = f"Password reset link: http://localhost:8000/auth/reset-password?token={reset_token}"

        response = ses_client.send_email(
            Source=f"{AWS_EMAIL_SENDER}",
            Destination={"ToAddresses": [email]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        return response

    def store_reset_token(self, email, token):
        self.storage.set(email, token)

    def get_reset_token(self, email):
        return self.storage.get(email).decode("utf-8")

    def store_jti(self, username, jti):
        self.storage.set(username, jti)

    def get_jti(self, username):
        return self.storage.get(username)

    def delete_token(self, email):
        self.storage.delete(email)

    def generate_and_send_reset_token(self, email):
        reset_token = self.generate_reset_password_token()

        self.send_reset_token(email, reset_token)

        self.store_reset_token(email, reset_token)

        return reset_token
