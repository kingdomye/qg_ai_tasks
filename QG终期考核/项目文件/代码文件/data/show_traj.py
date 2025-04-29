'''
----------------------------------------------------
# file:         show_traj.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  轨迹散点可视化
----------------------------------------------------
'''

import matplotlib.pyplot as plt
import json
from utils import PreProcess

data = './realistic_trajectories.json'
with open (data, 'r') as f:
    data = json.load(f)

data = PreProcess(data)

for car in data:
    for T in car['paths']:
        for i in range(len(T) - 1):
            point = T[i]
            coords = point['coords']
            next_point = T[i + 1]
            next_coords = next_point['coords']
            plt.plot([coords[0], next_coords[0]], [coords[1], next_coords[1]], color='blue')
plt.show()
