from django.db.models import Count
from rest_framework import viewsets

from utils.pagination import CursorPagination
from utils.permissions import UserPermission
from . import models
from . import serializers


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tag.objects.order_by('title')
    serializer_class = serializers.TagSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    lookup_field = 'code'
    queryset = models.Post.objects.filter(parent__isnull=True)
    permission_classes = (UserPermission,)
    pagination_class = CursorPagination

    def get_queryset(self):
        return self.queryset.annotate(
            answer_count=Count('children')
        ).order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.QuestionDetailSerializer
        if self.action == 'list':
            return serializers.QuestionListSerializer
        if self.action == 'create':
            return serializers.QuestionCreateUpdateSerializer
        if self.action == 'update':
            return serializers.QuestionCreateUpdateSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    lookup_field = 'code'
    queryset = models.Post.objects.filter(parent__isnull=False)
    permission_classes = (UserPermission,)

    def get_queryset(self):
        return self.queryset.order_by('rating', 'created_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AnswerListSerializer
        if self.action == 'list':
            return serializers.AnswerListSerializer
        if self.action == 'create':
            return serializers.AnswerCreateUpdateSerializer
        if self.action == 'update':
            return serializers.AnswerCreateUpdateSerializer
