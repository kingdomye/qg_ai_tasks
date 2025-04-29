'''
----------------------------------------------------
# file:         PreProcess.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  数据预处理，时空筛选、数据抽样、MDL轨迹简化
----------------------------------------------------
'''

import numpy as np

class PreProcess:
    def __init__(self, D, time_range=None, location_range=None, sample_ratio=1.0, epsilon=1e-3):
        self.D = D
        self.time_range = time_range
        self.location_range = location_range
        self.sample_ratio = sample_ratio
        self.epsilon = epsilon
        self.D_s = self.main()

    def filter_trajectory(self):
        D_filtered = []
        for T in self.D:
            if self.time_range:
                start_time, end_time = self.time_range
                T = [p for p in T if (start_time <= p[2] <= end_time)]
            if self.location_range:
                min_x, max_x, min_y, max_y = self.location_range
                T = [p for p in T if (min_x <= p[0] <= max_x) and (min_y <= p[1] <= max_y)]
            if len(T) > 0:
                D_filtered.append(T)
        
        D_filtered = np.array(D_filtered, dtype=object)

        if self.sample_ratio < 1.0:
            D_filtered = np.random.choice(D_filtered, int(len(D_filtered) * self.sample_ratio), replace=False).tolist()

        return D_filtered
    
    def simplify_mdl(self, T):
        def point_to_line_distance(p, p1, p2):
                x, y = p[0], p[1]
                x1, y1 = p1[0], p1[1]
                x2, y2 = p2[0], p2[1]
                return np.abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / np.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        
        if len(T) <= 2:
            return T
            
        key_indices = [0, len(T) - 1]
        def _mdl(start, end):
            if end - start <= 1:
                return
                
            p_start, p_end = T[start], T[end]
            max_error = 0
            best_idx = start + 1

            for i in range(start + 1, end):
                error = point_to_line_distance(T[i], p_start, p_end)
                if error > max_error:
                    max_error = error
                    best_idx = i

            if max_error > self.epsilon:
                key_indices.append(best_idx)
                _mdl(start, best_idx)
                _mdl(best_idx, end)
                
        _mdl(0, len(T) - 1)
        T_simplified = [T[i] for i in sorted(key_indices)]

        return T_simplified
    
    def main(self):
        D_filtered = self.filter_trajectory()
        D_s = [self.simplify_mdl(T) for T in D_filtered]
        return D_s

