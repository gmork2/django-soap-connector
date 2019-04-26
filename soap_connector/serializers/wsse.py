import os

from rest_framework import serializers

from .base import BaseSerializer

DEFAULT_PATH = os.path.join(os.getenv("HOME"))


class SignatureSerializer(BaseSerializer):
    """

    """
    key_data = serializers.FilePathField(path=DEFAULT_PATH)
    cert_data = serializers.FilePathField(path=DEFAULT_PATH)
    password = serializers.CharField()


class UsernameTokenSerializer(BaseSerializer):
    """

    """
    username = serializers.CharField()
    password = serializers.CharField()
    password_digest = None
    nonce = None
    created = None
    use_digest = None
    timestamp_token = None
