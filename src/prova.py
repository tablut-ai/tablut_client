import numpy as np 

a = np.array([[0,3], [0,4], [0,5], [1,4], [8,3], [8,4], [8,5], [7,4]])
t = np.array([[4,4],[0,4]])

print(np.array_equal(a[1], t))

print(((t[1] == a).all(axis=(1))).any())