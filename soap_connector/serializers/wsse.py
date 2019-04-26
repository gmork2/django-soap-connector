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
