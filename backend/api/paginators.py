from rest_framework.pagination import PageNumberPagination


class PaginationWithLimit(PageNumberPagination):
    page_size_query_param = 'limit'
