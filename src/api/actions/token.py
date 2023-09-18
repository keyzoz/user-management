import random
import string

import boto3

from settings import localstack_endpoint_url
from src.db.redis_db import get_redis_client


class ResetTokenService:
    def __init__(self):
        self._storage = None

    @property
    def redis_storage(self):
        if self._storage is None:
            self._storage = get_redis_client()
        return self._storage

    @redis_storage.setter
    def redis_storage(self, value):
        self._storage = value

    @staticmethod
    def generate_reset_password_token(length: int = 32):
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    @staticmethod
    def send_reset_token(email: str, reset_token):
        ses_client = boto3.client(
            "ses",
            region_name="us-east-1",
            endpoint_url=localstack_endpoint_url,
        )

        subject = "Reset Password"
        body = f"Password reset link: http://localhost:8000/auth/reset-password?token={reset_token}"

        response = ses_client.send_email(
            Source="user1@yourdomain.com",
            Destination={"ToAddresses": [email]},
            Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        )
        return response

    def store_reset_token(self, email, token):
        self._storage.set(email, token)

    def get_reset_token(self, email):
        return self._storage.get(email).decode("utf-8")

    def store_jti(self, username, jti):
        self._storage.set(username, jti)

    def get_jti(self, username):
        return self._storage.get(username)

    def delete_token(self, email):
        self._storage.delete(email)

    def generate_and_send_reset_token(self, email):
        reset_token = self.generate_reset_password_token()

        self.send_reset_token(email, reset_token)

        self.store_reset_token(email, reset_token)

        return reset_token
