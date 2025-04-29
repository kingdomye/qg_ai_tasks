'''
----------------------------------------------------
# file:         show_traj.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  绘制轨迹散点图
----------------------------------------------------
'''

import matplotlib.pyplot as plt
import json
from PreProcess import PreProcess

data = '../data/realistic_trajectories.json'
with open (data, 'r') as f:
    data = json.load(f)

for D in data:
    for T in D['paths']:
        for i in range(len(T)-1):
            cur_point, next_point = T[i], T[i+1]
            cur_coords, next_coords = cur_point['coords'], next_point['coords']
            plt.plot([cur_coords[1], next_coords[1]], [cur_coords[0], next_coords[0]], color='blue')
plt.show()
