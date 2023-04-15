from rest_framework.pagination import PageNumberPagination

class OrderPagination(PageNumberPagination):
    page_size = 2
    page_sizer_query_param = 'paginate_by'
    max_page_size = 6