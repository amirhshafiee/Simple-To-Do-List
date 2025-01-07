from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    description = serializers.CharField()
    active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        task = Task.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            active = validated_data['active'],
            author = validated_data['user'],
        )

        return task

class ShowTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ['author', 'id', ]
        extra_kwargs = {
            'create_time': {'read_only': True},
        }