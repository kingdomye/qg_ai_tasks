'''
----------------------------------------------------
# file:         WeightedDp.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  加权差分隐私分配
----------------------------------------------------
'''

import numpy as np

class WeightedDp:
    def __init__(self, D_m, G, r, E_1_matrix, epsilon_1, epsilon_2, epsilon_3, epsilon_4):
        self.D_m = D_m
        self.G = G
        self.r = r
        self.E_1_matrix = E_1_matrix
        self.E_2_matrix = None
        self.epsilon_1 = epsilon_1
        self.epsilon_2 = epsilon_2
        self.epsilon_3 = epsilon_3
        self.epsilon_4 = epsilon_4
        self.grids_indices = None

        self.output = self.main()

        # 构建概率分布
    def main(self):
        '''
        :param D_m: 映射后的数据集
        :param G: 网络结构
        :param r: 分辨率向量
        :param E_1_matrix: 补充预算矩阵
        :param epsilon_2、3、4: 预定义的预算
        :return D_r: 重建后的数据集
        '''
        # 参数w计算
        leaf_grids = []
        def _collect_leaves(cell):
            if cell.is_leaf():
                leaf_grids.append(cell)
            else:
                for child in cell.children:
                    _collect_leaves(child)

        _collect_leaves(self.G)
        grids_indices = {id(grid): idx for idx, grid in enumerate(leaf_grids)}
        g_dict = {idx: cell for idx, cell in enumerate(leaf_grids)}
            
        weights = np.ones(len(self.r)) / len(self.r)

        #==============================
        # 行程分布提取，分配预算矩阵E_2
        #==============================
        E_2_matrix = np.diag((1 - weights) * self.epsilon_2)
        diag_elements = np.diag(E_2_matrix)
        min_matrix = np.minimum(diag_elements[:, None], diag_elements[None, :])
        E_2_matrix = np.where(np.eye(len(self.r)), E_2_matrix, min_matrix)
        
        # 补充预算矩阵E_2'
        E_2_matrix_prime = np.ones_like(self.E_1_matrix) * self.epsilon_2
        diag_elements = np.diag(E_2_matrix)
        min_matrix = np.minimum(diag_elements[:, None], diag_elements[None, :])
        E_2_matrix_prime -= min_matrix

        # 行程分布提取
        def extract_trip_distribution(D_m, weights):
            n_grids = len(weights)
            trip_counts = np.zeros((n_grids, n_grids))
            
            for T in D_m:
                start, end = grids_indices[id(T[0])], grids_indices[id(T[-1])]
                trip_counts[start][end] += 1
            
            noise = np.random.laplace(scale=E_2_matrix)
            trip_counts += noise
            trip_counts = np.maximum(trip_counts, 0)
            return trip_counts
        trip_counts = extract_trip_distribution(self.D_m, weights)
        
        #==============================
        # 移动模型构建，计算分配预算矩阵E_3
        #==============================
        E_3_matrix = np.zeros_like(self.E_1_matrix)
        diag_elements = self.epsilon_1 + self.epsilon_2 + self.epsilon_3 - self.r - np.diag(E_2_matrix)
        np.fill_diagonal(E_3_matrix, diag_elements)
        min_matrix = np.minimum(diag_elements[:, None], diag_elements[None, :])
        E_3_matrix += np.where(np.eye(len(self.r)), 0, min_matrix)

        # 移动模型构建
        def build_mobility_model(D_m):
            n_grids = len(E_2_matrix_prime)
            transition_matrix = np.zeros((n_grids, n_grids))

            for T in D_m:
                for k in range(len(T) - 1):
                    i, j = grids_indices[id(T[k])], grids_indices[id(T[k + 1])]
                    transition_matrix[i][j] += 1

            noise = np.random.laplace(scale=self.E_1_matrix + E_2_matrix_prime + self.epsilon_3)
            transition_matrix += noise
            transition_matrix = np.maximum(transition_matrix, 0)
            transition_matrix_noisy = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)
            return transition_matrix_noisy
        transition_matrix_noisy = build_mobility_model(self.D_m)
        
        #==============================
        # 路线长度估计，计算分配预算向量E_4
        #==============================
        def estimate_route_length(D_m):
            lengths = [len(T) for T in D_m]
            epsilon_4_vector = np.full(len(lengths), self.epsilon_4)
            for i in range(len(lengths)):
                scale = 1 / self.epsilon_4
                noise = np.random.laplace(scale=scale)
                lengths[i] += noise
                lengths[i] = max(1, lengths[i])
            return lengths
        
        length_distribution = estimate_route_length(self.D_m)
        
        #==============================
        # 合成轨迹生成D_r
        #==============================
        def generate_synthetic_trajectories(trip_counts, transition_matrix, length_distribution):
            def sample_start_end(trip_counts):
                counts = trip_counts.flatten()
                probs = counts / np.sum(counts)
                idx = np.random.choice(len(probs), p=probs)
                n = trip_counts.shape[0]
                start, end = idx // n, idx % n
                return start, end
            
            D_r = []
            total_T = int(np.sum(trip_counts))

            for _ in range(total_T):
                start, end = sample_start_end(trip_counts)
                length = int(np.random.choice(length_distribution))

                T = [start]
                cur = start
                for _ in range(length - 1):
                    next_grid = np.random.choice(len(trip_counts), p=transition_matrix[cur])
                    T.append(next_grid)
                    cur = next_grid

                T[-1] = end
                D_r.append(T)

            return D_r

        D_r = generate_synthetic_trajectories(trip_counts, transition_matrix_noisy, length_distribution)
        return D_r, g_dict