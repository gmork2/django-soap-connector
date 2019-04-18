import logging
from typing import Dict, Union

logger = logging.getLogger(__name__)

Context = Dict[
    str,
    Union[
        "api.base.BaseAPIView",
        "rest_framework.request.Request"
    ]
]
