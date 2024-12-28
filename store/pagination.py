from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class DefaultPagination(PageNumberPagination):
    page_size = 10