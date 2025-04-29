'''
----------------------------------------------------
# file:         DataLayer.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  主函数，对应论文的LogicLayer逻辑处理层
----------------------------------------------------
'''

from GZTaxiData import GZTaxiData
import numpy as np
from PreProcess import PreProcess
from MultiResolutionAg import MultiResolutionAg
from WeightedDp import WeightedDp
from ContinuityMaintenance import ContinuityMaintenance
from GridCell import GridCell

from matplotlib import pyplot as plt

class Datalayer:
    def __init__(self, file_path='../data/real_trajectory.json'):
        self.data = GZTaxiData(file_path)
        self.cars = self.data.dataset()
        self.D = self.cars.copy()
        self.random_seed = 0
    
    def process_single(self, D, epsilon, d, rho=2.0):
        epsilon_1, epsilon_2, epsilon_3, epsilon_4 = epsilon * (1/9), epsilon * (3/9), epsilon * (4/9), epsilon * (1/9)
        D_s = PreProcess(D).D_s
        D_m, G, r, E_1, E_1_matrix = MultiResolutionAg(D_s, epsilon_1=epsilon_1, d=d, rho_0=rho).output
        D_r, g_dict = WeightedDp(D_m, G, r, E_1_matrix, epsilon_1=epsilon_1, epsilon_2=epsilon_2, epsilon_3=epsilon_3, epsilon_4=epsilon_4).output
        D_processed = ContinuityMaintenance(D_r, g_dict, 12).output
        
        D_processed_coord = []
        for T in D_processed:
            T_coord = [((g_dict[i].bounds[0] + g_dict[i].bounds[2]) / 2, (g_dict[i].bounds[1] + g_dict[i].bounds[3]) / 2) for i in T]
            D_processed_coord.append(T_coord)

        return D_processed, D_processed_coord
    
    def process(self, epsilon=1, d=2, rho=2.0):
        D_processed_all, D_processed_coord_all = [], []
        all_points = []
        for i in range(len(self.D)):
            np.random.seed(self.random_seed)
            D_processed, D_processed_coord = self.process_single(self.D[i], epsilon, d, rho)
            D_processed_all.append(D_processed)
            D_processed_coord_all.append(D_processed_coord)
        
        for D in self.D:
            for T in D:
                for point in T:
                    all_points.append(point)

        G = self.split_G(all_points, epsilon, d)

        return D_processed_all, D_processed_coord_all, G
    
    def split_G(self, all_points, epsilon, d, rho=2.0):
        min_x, max_x = min([point[0] for point in all_points]), max([point[0] for point in all_points])
        min_y, max_y = min([point[1] for point in all_points]), max([point[1] for point in all_points])
        bounds = [min_x, min_y, max_x, max_y]
        G = GridCell(bounds)
        h_max = int(np.ceil(0.5 * np.log(len(all_points)) / np.log(d)))
        epsilon_r = epsilon / h_max

        h = 1
        while h <= h_max:
            new_partitions = False
            leaf_cells = G.get_all_leaf_cells()

            for cell in leaf_cells:
                n_i = sum([1 for point in all_points if cell.contains(point)])
                n_i_prime = n_i + np.random.laplace(0, 1 / epsilon_r)

                if n_i_prime > rho:
                    cell.split(d)
                    new_partitions = True

            if not new_partitions:
                break

            h += 1

        return G


if __name__ == '__main__':
    epsilon = 2
    d = 2
    rho = 2
    np.random.seed(0)

    datalayer = Datalayer()
    D = datalayer.D
    for d in D:
        for T in d:
            for point in T:
                plt.scatter(point[0], point[1], color='blue', s=20)
    D_p, D_p_c, G= datalayer.process(epsilon=epsilon, d=2, rho=rho)
    for d in D_p_c:
        for T in d:
            for point in T:
                plt.scatter(point[0], point[1], color='red', s=20)
    G.show(G)
    plt.show()
    