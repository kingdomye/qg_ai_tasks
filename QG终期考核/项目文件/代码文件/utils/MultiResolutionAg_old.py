'''
----------------------------------------------------
# file:         MultiResolutionAg_old.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  多分辨率自适应网络构建，这是第一个版本，在部分场景中有问题，暂存
----------------------------------------------------
'''

import numpy as np
from GridCell import GridCell
import numpy as np

class MultiResolutionAg:
    def __init__(self, D_s, epsilon_1, d, rho_0=2.0):
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

        # 递归划分网格
        def _split_cell(cell, current_h):
            if current_h >= h_max:
                return
            
            cell.trajectory_points = [
                p for T in self.D_s for p in T 
                if (cell.bounds[0] <= p[0] <= cell.bounds[2]) and 
                (cell.bounds[1] <= p[1] <= cell.bounds[3])
            ]

            n_i = sum(len([p for p in traj if p in cell.trajectory_points]) / len(traj) for traj in self.D_s)
            n_i_prime = n_i + np.random.laplace(scale=1/epsilon_r)

            if n_i_prime > self.rho_0:
                cell.split(self.d)
                for child in cell.children:
                    _split_cell(child, current_h + 1)

        _split_cell(G, 0)

        # 计算函数返回值
        resolutions = []
        def _collect_resolutions(cell):
            if cell.is_leaf():
                resolutions.append(cell.resolution)
            else:
                for child in cell.children:
                    _collect_resolutions(child)

        _collect_resolutions(G)

        r = np.array(resolutions)
        E_1 = r * epsilon_r
        E_1_matrix = np.eye(len(r)) * self.epsilon_1
        E_1_matrix -= np.diag(E_1)
        for i in range(len(r)):
            for j in range(len(r)):
                if i != j:
                    E_1_matrix[i, j] = min(E_1_matrix[i, i], E_1_matrix[j, j])

        D_m = []
        for T in self.D_s:
            mapped_T = []
            for point in T:
                def _find_cell(cell, point):
                    if cell.is_leaf():
                        return cell
                    for child in cell.children:
                        if ((child.bounds[0] <= point[0] <= child.bounds[2]) and (child.bounds[1] <= point[1] <= child.bounds[3])):
                            return _find_cell(child, point)
                    print(f'not found cell for point {point}')
                    return -1
                cell_resolution = _find_cell(G, point)
                mapped_T.append(cell_resolution)
            D_m.append(mapped_T)

        return D_m, G, r, E_1, E_1_matrix
    