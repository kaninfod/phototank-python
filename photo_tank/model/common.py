__author__ = 'martin'



from math import ceil



class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def min_rec(self):
        return (self.page - 1) * self.per_page


    @property
    def max_rec(self):
        return min(self.page * self.per_page, self.total_count)


    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=1, left_current=2,
                   right_current=4, right_edge=1):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or (
                                    self.page - left_current - 1 < num < self.page + right_current) or num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


