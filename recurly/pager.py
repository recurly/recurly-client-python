class ItemIterator:
    def __init__(self, client, next_url, params):
        self.__page_iterator = PageIterator(client, next_url, params)
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

        return self.__data[self.__index]


class PageIterator:
    def __init__(self, client, next_url, params):
        self.__client = client
        self.__next_url = next_url
        self.__params = params
        self.__has_more = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.__has_more:
            page = self.__client._make_request(
                "GET", self.__next_url, None, self.__params
            )

            # We don't need the params anymore as they are
            # automatically set in __next_url
            if self.__params:
                self.__params = None

            self.__next_url = page.next
            self.__has_more = page.has_more
            return page.data
        else:
            raise StopIteration


class Pager:
    def __init__(self, client, path, params):
        self.__client = client
        self.__path = path
        self.__params = params

    def pages(self):
        return PageIterator(self.__client, self.__path, self.__params)

    def items(self):
        return ItemIterator(self.__client, self.__path, self.__params)
