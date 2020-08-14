import copy


class ItemIterator:
    def __init__(self, client, next_url, **options):
        self.__page_iterator = PageIterator(client, next_url, **options)
        self.__index = 0
        self.__data = None

    def __iter__(self):
        return self

    def __next__(self):
        # If we are in a page, get the next item
        if self.__data and self.__index < len(self.__data) - 1:
            self.__index += 1
        # else we want to fetch a new page and point to the first item
        else:
            self.__data = next(self.__page_iterator)
            self.__index = 0

        if len(self.__data) > 0:
            return self.__data[self.__index]
        else:
            raise StopIteration


class PageIterator:
    def __init__(self, client, next_url, **options):
        self.__client = client
        self.__next_url = next_url
        self.__options = options
        self.__has_more = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.__has_more:
            page = self.__client._make_request(
                "GET", self.__next_url, None, **self.__options
            )

            # We don't need the params anymore as they are
            # automatically set in __next_url
            if "params" in self.__options:
                del self.__options["params"]

            self.__next_url = page.next
            self.__has_more = page.has_more
            return page.data
        else:
            raise StopIteration


class Pager:
    def __init__(self, client, path, **options):
        self.__client = client
        self.__path = path
        self.__options = options

    def pages(self):
        """An iterator that enumerates each page of results."""
        return PageIterator(self.__client, self.__path, **self.__options)

    def items(self):
        """An iterator that enumerates each item on the server and paginates
        under the hood.
        """
        return ItemIterator(self.__client, self.__path, **self.__options)

    def first(self):
        """Performs a request with the pager `limit` set to 1 and only returns the
        first result in the response.
        """
        options = self.__options
        if "params" in options:
            options = copy.deepcopy(options)
            options["params"].update({"limit": 1})
        items = ItemIterator(self.__client, self.__path, **options)
        try:
            return next(items)
        except StopIteration:
            return None

    def take(self, n):
        """Performs a request with the pager `limit` set to `n` and only returns the
        first `n` results in the response. `n` is limited to the maximum page size.
        """
        options = self.__options
        if "params" in options:
            options = copy.deepcopy(options)
            options["params"].update({"limit": n})
        items = PageIterator(self.__client, self.__path, **options)
        try:
            return next(items)
        except StopIteration:
            return None

    def count(self):
        """Makes a HEAD request to the API to determine how many total records exist.
        """
        resource = self.__client._make_request(
            "HEAD", self.__path, None, **self.__options
        )
        return resource.get_response().total_records
