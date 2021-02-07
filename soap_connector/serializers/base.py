from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    """

    """
    pk = serializers.IntegerField(default=1, min_value=1)

    def validate(self, data: dict) -> dict:
        """

        :param data:
        :return:
        """
        view = self.context['view']
        items = view.cache.registry.retrieve()
        data['pk'] = items[-1] + 1 if items else 1

        return data

    def save(self, validated_data: dict) -> dict:
        """

        :param validated_data:
        :return:
        """
        view = self.context['view']
        pk = validated_data['pk']
        view.cache[pk] = validated_data

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
