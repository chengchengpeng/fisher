A = {'a': '1'}

a = A.setdefault('a', 'a1')
b = A.setdefault('b', 'b2')
print(a)
print(b)
print(A)