from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.serializers import ProfileSerializer
from . import models


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'title',)


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
        fields = ('code', 'body', 'rating', 'created_at', 'updated_at', 'author')


class AnswerCreateSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(source='parent.code')

    class Meta:
        model = models.Post
        fields = ('code', 'body', 'parent')
        read_only_fields = ('code',)

    def create(self, validated_data):
        parent = validated_data.pop('parent')
        parent_code = parent.get('code')
        parent_obj = get_object_or_404(models.Post, code=parent_code)
        validated_data['author'] = self.context['request'].user.profile
        validated_data['post_type'] = models.PostChoices.ANSWER
        validated_data['parent_id'] = parent_obj.pk
        return self.Meta.model.objects.create(**validated_data)


class AnswerUpdateSerializer(AnswerCreateSerializer):
    parent = serializers.CharField(required=False)

    class Meta(AnswerCreateSerializer.Meta):
        fields = ('code', 'body', 'parent')

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class QuestionDetailSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    tags = TagSerializer(many=True)
    answer_count = serializers.IntegerField()
    answers = AnswerListSerializer(source='children', many=True)

    class Meta:
        model = models.Post
        exclude = ('id',)
