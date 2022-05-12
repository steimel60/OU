l = [x for x in range(100)]

groups = 4

nbrs = []

for i in range(groups):
    nbrs.append(l[i::groups])

for n in nbrs:
    print(n)
