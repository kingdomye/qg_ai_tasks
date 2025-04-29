'''
----------------------------------------------------
# file:         GZTaxiData.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  统一的数据读取接口
----------------------------------------------------
'''

import json
import numpy as np
from matplotlib import pyplot as plt

class GZTaxiData:
    def __init__(self, file_path='../data/trajectory.json'):
        self.file_path = file_path
        self.data = self._load_data()
    
    def _load_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
    
    def dataset(self):
        D = [
            [[(p['coords'][0], p['coords'][1], p['timestamp']) for p in path] 
             for path in car['paths']]
            for car in self.data
        ]
        return D

if __name__ == '__main__':
    data = GZTaxiData()
    cars = data.dataset()
    print(len(cars))