from rest_framework import serializers
from .models import Rubric, Bb


class RubricSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rubric
        fields = ('id', 'name')


class BboardSerialiser(serializers.ModelSerializer):
    rubric = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Bb
        fields = ('published', 'content', 'rubric',)
