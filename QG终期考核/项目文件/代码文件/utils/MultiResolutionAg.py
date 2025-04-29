'''
----------------------------------------------------
# file:         MultiResolutionAg.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  多分辨率自适应网络构建优化版本，在实验过程中发现这个版本的代码更符合预期，因此选择这个版本
----------------------------------------------------
'''

import numpy as np
from GridCell import GridCell
import numpy as np

class MultiResolutionAg:
    def __init__(self, D_s, epsilon_1, d, rho_0=20.0):
        self.D_s = D_s
        self.epsilon_1 = epsilon_1
        self.d = d
        self.rho_0 = rho_0
        self.output = self.main()

    def main(self):
        # 参数初始化
        h_max = int(np.ceil(0.5 * np.log(len(self.D_s)) / np.log(self.d)))
        epsilon_r = self.epsilon_1 / h_max

        # 网格结构构建
        all_points = [point for T in self.D_s for point in T]
        min_x, max_x = min(p[0] for p in all_points), max(p[0] for p in all_points)
        min_y, max_y = min(p[1] for p in all_points), max(p[1] for p in all_points)
        bounds = [min_x, min_y, max_x, max_y]
        G = GridCell(bounds)

        E_bar_1 = np.diag([self.epsilon_1] * 1)

        h = 1
        while h <= h_max:
            new_partitions = False
            leaf_cells = G.get_all_leaf_cells()

            for cell in leaf_cells:
                n_i = sum(1 / len(T) for T in self.D_s for point in T if cell.contains(point))
                n_i_prime = n_i + np.random.laplace(0, 1 / epsilon_r)
                if n_i_prime > self.rho_0:
                    cell.split(self.d)
                    new_partitions = True

                    new_size = len(G.get_all_leaf_cells())
                    if new_size > E_bar_1.shape[0]:
                        old_size = E_bar_1.shape[0]
                        new_E_bar_1 = np.zeros((new_size, new_size))
                        new_E_bar_1[:old_size, :old_size] = E_bar_1
                        new_E_bar_1[old_size:, old_size:] = self.epsilon_1
                        E_bar_1 = new_E_bar_1
                
            if not new_partitions:
                break
            h += 1

        leaf_cells = G.get_all_leaf_cells()
        r = [cell.resolution for cell in leaf_cells]
        r = np.array(r)
        E_1 = np.array([ri * epsilon_r for ri in r])

        for i in range(len(E_1)):
            E_bar_1[i, i] = E_1[i]

        for i in range(len(E_1)):
            for j in range(len(E_1)):
                E_bar_1[i, j] = min(E_bar_1[i, i], E_bar_1[j, j])

        D_m = []
        for T in self.D_s:
            mapped_T = []
            for point in T:
                cell = G.map_point_to_cell(point)
                mapped_T.append(cell)
            D_m.append(mapped_T)

        return D_m, G, r, E_1, E_bar_1