
import pandas as pd

a = ['a', 'b', 'c', 'd']
id = 12
col = ['ca', 'cb', 'cc', 'cd']
d1 = pd.DataFrame(data=[a], index=[id], columns=col)
d1.index.name = 'FF'
pd1 = d1.copy()
a1 = ['a1', 'b1', 'c1', 'd1']
id1 = 6
col = ['ca', 'cb', 'cc', 'cd']
d2 = pd.DataFrame(data=[a1], index=[id1], columns=col)
p2d1 = pd1
pd1 = pd1.append(d2)
d1 = pd.concat([d1, d2])
d1 = pd.concat([d1, d2])
d1 = pd.concat([d1, d2])
d1 = pd.concat([d1, d2])
d1 = pd.concat([d1, d2])
print("something")



