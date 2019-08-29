class A:
    def __init__(self):
        self.data = [1, 2, 3, 4, 5]

    @property
    def first(self):
        return self.data[0] if self.data != [] else None

    # @property
    # def first(self):
    #     return self.book[0] if self.total > 0 else None


b = A()
print(b.first)