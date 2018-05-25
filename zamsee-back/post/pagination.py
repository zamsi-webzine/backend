from rest_framework.pagination import PageNumberPagination


class PostPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page'
    max_page_size = 10000
