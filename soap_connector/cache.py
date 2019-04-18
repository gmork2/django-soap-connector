import logging
from typing import Dict, Union

from django.core.cache import cache

logger = logging.getLogger(__name__)

Context = Dict[
    str,
    Union[
        "api.base.BaseAPIView",
        "rest_framework.request.Request"
    ]
]


def make_key(context, sufix: str) -> str:
    """

    :return:
    """
    return ':'.join([
        str(context['request'].user.id),
        sufix
    ])

