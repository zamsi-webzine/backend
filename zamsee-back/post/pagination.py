from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    page_size = 6
    page_query_param = 'page'
    max_page_size = 100


class ClientPostPagination(PageNumberPagination):
    page_size = 21
    page_query_param = 'page'
    max_page_size = 100
