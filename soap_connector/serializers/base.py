from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from soap_connector.cache import Cache

ERROR = _("Resource <{}> already exists.")


class BaseSerializer(serializers.Serializer):
    """

        """
    pk = serializers.IntegerField(default=1, min_value=1)

    def validate(self, data: dict) -> dict:
        """

        :param data:
        :return:
        """
        request = self.context['request']
        view = self.context['view']

        if request.method.upper() == 'POST':

            pk = data.get('pk')
            if pk in view.cache:
                msg = _(ERROR.format(pk))
                raise serializers.ValidationError(msg)

        return data

    def save(self, validated_data: dict) -> dict:
        """

        :param validated_data:
        :return:
        """
        pk = validated_data.get('pk')

        cache = Cache(self.context)
        cache[pk] = validated_data

        return validated_data

    def create(self, validated_data: dict) -> dict:
        """

        :param validated_data:
        :return:
        """
        return self.save(validated_data)

    def update(self, pk, validated_data: dict) -> dict:
        """

        :param pk:
        :param validated_data:
        :return:
        """
        view = self.context['view']
        validated_data['pk'] = view.kwargs['pk']

        return self.save(validated_data)
