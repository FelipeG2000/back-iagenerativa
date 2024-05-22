from rest_framework import serializers

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    question = serializers.CharField(max_length=4096)
    respuesta = serializers.CharField(max_length=4096)

    class Meta:
        model = Question
        fields = ['question', 'respuesta']