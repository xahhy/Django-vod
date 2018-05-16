from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CustomPaginator(Paginator):
    def __init__(self, current_page=0, per_pager_num=5, *args, **kwargs):
        # 当前页
        self.current_page = int(current_page)
        # 最多显示的页码数量
        self.per_pager_num = int(per_pager_num)
        super(CustomPaginator, self).__init__(*args, **kwargs)

    def pager_num_range(self):
        if self.num_pages < self.per_pager_num:
            return list(range(1, self.num_pages + 1))
        # 如果页数特别多
        part = int(self.per_pager_num / 2)
        if self.current_page <= part:
            return list(range(1, self.per_pager_num + 1))
        if (self.current_page + part) > self.num_pages:
            return list(range(self.num_pages - self.per_pager_num + 1, self.num_pages + 1))
        return list(range(self.current_page - part, self.current_page + part + 1))
