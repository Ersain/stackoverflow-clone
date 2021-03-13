from django.db.transaction import atomic
from rest_framework import serializers

from users.serializers import ProfileSerializer
from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'title',)


class QuestionDetailSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = models.Post
        exclude = ('id',)


class QuestionListSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    tags = TagSerializer(many=True)
    answer_count = serializers.IntegerField()

    class Meta:
        model = models.Post
        fields = ('code', 'title', 'rating', 'tags', 'created_at', 'answer_count', 'author')


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('code', 'title', 'body', 'tags')
        extra_kwargs = {
            'tags': {
                'allow_empty': True
            }
        }

    @atomic
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        validated_data['post_type'] = models.PostChoices.QUESTION
        tags = validated_data.pop('tags', [])
        instance = self.Meta.model.objects.create(**validated_data)
        instance.tags.set(tags)
        return instance

    @atomic
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        instance.tags.set(
            validated_data.get('tags', instance.tags.all())
        )
        return instance


class AnswerListSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = models.Post
        fields = ('code', 'title', 'body', 'rating', 'created_at', 'updated_at', 'author')


class AnswerCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('code', 'title', 'body')

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user.profile
        validated_data['post_type'] = models.PostChoices.ANSWER
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance
