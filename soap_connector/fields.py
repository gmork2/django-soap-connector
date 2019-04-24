from rest_framework.relations import HyperlinkedIdentityField


class HyperlinkedField(HyperlinkedIdentityField):
    """
    A read-only field that represents the identity URL for an object, itself.

    This is in contrast to `HyperlinkedRelatedField` which represents the
    URL of relationships to other objects.
    """
    lookup_field = 'pk'

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        lookup_value = obj[self.lookup_field]
        kwargs = {self.lookup_url_kwarg: lookup_value}

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
