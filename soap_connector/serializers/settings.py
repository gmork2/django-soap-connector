from rest_framework import serializers

from .base import BaseSerializer


class SettingsSerializer(BaseSerializer):
    """

    """
    strict = serializers.BooleanField(
        default=True,
        help_text="Boolean to indicate if the lxml should be parsed a ‘strict’."
                  "If false then the recover mode is enabled which tries to parse"
                  "invalid XML as best as it can.")

    raw_response = serializers.BooleanField(
        default=False,
        help_text="Boolean to skip the parsing of the XML response by zeep but"
                  "instead returning the raw data")

    forbid_dtd = serializers.BooleanField(
        default=False,
        help_text="Disallow XML with a <!DOCTYPE> processing instruction")

    forbid_entities = serializers.BooleanField(
        default=True,
        help_text="Disallow XML with <!ENTITY> declarations inside the DTD")

    forbid_external = serializers.BooleanField(
        default=True,
        help_text="Disallow any access to remote or local resources in external"
                  "entities or DTD and raising an ExternalReferenceForbidden"
                  "exception when a DTD or entity references an external resource.")

    xml_huge_tree = serializers.BooleanField(
        default=False,
        help_text="Disable lxml/libxml2 security restrictions and support very deep"
                  "trees and very long text content")

    force_https = serializers.BooleanField(
        default=True,
        help_text="Force all connections to HTTPS if the WSDL is also loaded from an"
                  "HTTPS endpoint. (default: true)")

    extra_http_headers = serializers.ListField(
        required=False,
        child=serializers.CharField(),
        help_text="Additional HTTP headers to be sent to the transport. This"
                  "can be used in combination with the context manager approach"
                  "to add http headers for specific calls.")

    xsd_ignore_sequence_order = serializers.BooleanField(
        help_text="Boolean to indicate whether to enforce sequence order when parsing"
                  "complex types. This is a workaround for servers that don’t respect"
                  "sequence order.")
    tls = ""
