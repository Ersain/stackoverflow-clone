from rest_framework.pagination import (
    CursorPagination as BaseCursorPagination,
)


class CursorPagination(BaseCursorPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    ordering = '-created_at'
