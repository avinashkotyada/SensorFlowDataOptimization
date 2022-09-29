import numpy as np
import pandas as pd

df = pd.read_csv("Survey1.csv")
arr = np.array(df)
dis_yes = {'Egret': 0, 'Dedhar': 0, 'Breag': 0, 'Canary': 0}
dis_no = {'Egret': 0, 'Dedhar': 0, 'Breag': 0, 'Canary': 0}

for ar in arr:
    if ar[6] == 'Yes':
        dis_yes[ar[5]] = dis_yes[ar[5]] + 1
    else:
        dis_no[ar[5]] = dis_no[ar[5]] + 1

for i in dis_yes:
    print(i, end=" ")
    print(dis_yes[i], end=" ")
    print(dis_no[i])
