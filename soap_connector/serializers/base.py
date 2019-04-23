from rest_framework import serializers

ERROR = "Resource <{}> already exists."


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
            if pk in view.cache():
                msg = _(ERROR.format(pk))
                raise serializers.ValidationError(msg)

        return data

    def save(self, validated_data: dict) -> dict:
        """

        :param validated_data:
        :return:
        """
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
        return self.save(validated_data)
