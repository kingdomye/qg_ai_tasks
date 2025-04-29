'''
----------------------------------------------------
# file:         Evaluate.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  五项指标评估
----------------------------------------------------
'''

from DataLayer import Datalayer
import numpy as np
from collections import defaultdict
from scipy.stats import entropy
from matplotlib import pyplot as plt

class Evaluate:
    def __init__(self, epsilon, d):
        datalayer = Datalayer()
        self.D = datalayer.D
        self.D_processed, self.D_processed_coord, self.G= datalayer.process(epsilon, d)
        
    def RE(self):
        def calculate_re(start_point, end_point, radius, original_T, synthetic_T):
            point_row = np.random.uniform(start_point[0], end_point[0])
            point_col = np.random.uniform(start_point[1], end_point[1])

            count_d, count_sd = 0, 0

            for T in original_T:
                for point in T:
                    if (point[0] - point_row)**2 + (point[1] - point_col)**2 <= radius**2:
                        count_d += 1
                        break

            for T in synthetic_T:
                for point in T:
                    if (point[0][0] - point_row)**2 + (point[0][1] - point_col)**2 <= radius**2:
                        count_sd += 1
                        break

            b = len(original_T) * 0.001

            return b, count_d, count_sd
        
        def compute_average_RE(original_D, synthetic_D):
            total_b = 0
            total_count_d = 0
            total_count_sd = 0

            for i in range(len(original_D)):
                for j in range(len(original_D[i])):
                    b, count_d, count_sd = calculate_re(
                        original_D[i][j][0],
                        original_D[i][j][-1],
                        0.2,
                        original_D[i],
                        synthetic_D
                    )
                    total_b += b
                    total_count_d += count_d
                    total_count_sd += count_sd
            
            re = abs(total_count_sd - total_count_d) / max(total_count_d, total_b)

            return re

        RE = compute_average_RE(self.D, self.D_processed_coord)
        
        return RE
        
    def FPS_KT(self):
        def calculate_fps_kt(original_D, synthetic_D, grid_side=6, min_pattern_length=3, top_patterns=50):
            all_points = [point for T in original_D + synthetic_D for point in T]
            min_x = min(point[0] for point in all_points)
            max_x = max(point[0] for point in all_points)
            min_y = min(point[1] for point in all_points)
            max_y = max(point[1] for point in all_points)
            x_span = max_x - min_x
            y_span = max_y - min_y

            # 坐标转网格编号
            def point_to_grid(point):
                x, y = point[0], point[1]
                x_grid = int((x - min_x) / (x_span / grid_side))
                y_grid = int((y - min_y) / (y_span / grid_side))
                return x_grid * grid_side + y_grid
            
            # 提取频繁模式
            def extract_patterns(D):
                patterns = defaultdict(int)
                for T in D:
                    grid_seq = []
                    prev_grid = None
                    for point in T:
                        curr_grid = point_to_grid(point)
                        if curr_grid != prev_grid:
                            grid_seq.append(curr_grid)
                            prev_grid = curr_grid
                    
                    for i in range(len(grid_seq)):
                        for j in range(i + min_pattern_length, min(i + 10, len(grid_seq)) + 1):
                            pattern = tuple(grid_seq[i:j])
                            patterns[pattern] += 1

                return patterns

            original_patterns = extract_patterns(original_D)
            synthetic_patterns = extract_patterns(synthetic_D)

            # 计算FPS指标
            matched = 0
            total_error = 0
            sorted_patterns = sorted(original_patterns.items(), key=lambda x: x[1], reverse=True)[:top_patterns]

            # 计算KT指标
            concordant = 0
            discordant = 0
            valid_pairs = 0

            common_patterns = []

            for pattern, count in sorted_patterns:
                if pattern in synthetic_patterns:
                    syn_count = synthetic_patterns[pattern]
                    relative_error = abs(count - syn_count) / max(count, 1)
                    total_error += relative_error
                    matched += 1

                    common_patterns.append(pattern)

            for i in range(len(common_patterns)):
                for j in range(i + 1, len(common_patterns)):
                    pattern_i = common_patterns[i]
                    pattern_j = common_patterns[j]

                    original_order = original_patterns[pattern_i] - original_patterns[pattern_j]
                    synthetic_order = synthetic_patterns[pattern_i] - synthetic_patterns[pattern_j]

                    if original_order * synthetic_order > 0:
                        concordant += 1
                    elif original_order * synthetic_order < 0:
                        discordant += 1
                    
                    valid_pairs += 1

            FPS = total_error / matched if matched > 0 else 1.0
            KT = (concordant - discordant) / valid_pairs if valid_pairs > 0 else 1.0

            return FPS, KT
        
        fps_score = 0
        kt_score = 0
        for i in range(len(self.D)):
            fps, kt = calculate_fps_kt(self.D[i], self.D_processed_coord[i])
            fps_score += fps
            kt_score += kt

        fps_score /= len(self.D)
        kt_score /= len(self.D)

        return fps_score, kt_score
        
    def DE(self):
        def js_divergence(p, q):
            p = np.asarray(p)
            q = np.asarray(q)
            m = 0.5 * (p + q)

            return 0.5 * (entropy(p, m) + entropy(q, m))
        
        def calculate_de(original_D, synthetic_D, grid_side=6):
            all_points = [point for T in original_D + synthetic_D for point in T]
            min_x = min(point[0] for point in all_points)
            max_x = max(point[0] for point in all_points)
            min_y = min(point[1] for point in all_points)
            max_y = max(point[1] for point in all_points)
            x_span = max_x - min_x
            y_span = max_y - min_y

            # 坐标转网格编号
            def point_to_grid(point):
                x, y = point[0], point[1]
                x_grid = int((x - min_x) / (x_span / grid_side))
                y_grid = int((y - min_y) / (y_span / grid_side))
                return x_grid * grid_side + y_grid
            
            # 构建网格分布直方图
            def build_grid_distribution(D):
                grid_counts = defaultdict(int)
                for T in D:
                    visited_grids = set()
                    for point in T:
                        grid = point_to_grid(point)
                        if grid not in visited_grids:
                            grid_counts[grid] += 1
                            visited_grids.add(grid)
                
                total = sum(grid_counts.values())
                return {grid: count / total for grid, count in grid_counts.items()}

            original_grid_distribution = build_grid_distribution(original_D)
            synthetic_grid_distribution = build_grid_distribution(synthetic_D)

            # 计算TE指标
            all_grids = set(original_grid_distribution.keys()).union(set(synthetic_grid_distribution.keys()))

            original_vec = []
            synthetic_vec = []

            for grid in all_grids:
                original_vec.append(original_grid_distribution.get(grid, 0))
                synthetic_vec.append(synthetic_grid_distribution.get(grid, 0))

            original_vec = np.array(original_vec)
            synthetic_vec = np.array(synthetic_vec)

            return original_vec, synthetic_vec
        
        ori_vecs, syn_vecs = [], []
        for i in range(len(self.D)):
            ori, syn = calculate_de(self.D[i], self.D_processed_coord[i])
            ori_vecs.extend(ori)
            syn_vecs.extend(syn)

        de_score = js_divergence(ori_vecs, syn_vecs)

        return de_score
    
    def TE(self):
        def js_divergence(p, q):
            p = np.asarray(p)
            q = np.asarray(q)
            m = 0.5 * (p + q)

            return 0.5 * (entropy(p, m) + entropy(q, m))
            
        def calculate_te(original_D, synthetic_D, n_grid=2):
            all_points = [point for T in original_D + synthetic_D for point in T]
            min_x = min(point[0] for point in all_points)
            max_x = max(point[0] for point in all_points)
            min_y = min(point[1] for point in all_points)
            max_y = max(point[1] for point in all_points)

            x_span = max_x - min_x
            y_span = max_y - min_y
            x_len = x_span / n_grid
            y_len = y_span / n_grid

            # 坐标转网格编号
            def point_to_grid(point):
                x, y = point[0], point[1]
                x_grid = int((x - min_x) / x_len)
                y_grid = int((y - min_y) / y_len)
                x_grid = min(n_grid - 1, max(0, x_grid))
                y_grid = min(n_grid - 1, max(0, y_grid))
                return x_grid * n_grid + y_grid
            
            def get_trip_distribution(D):
                trip_counts = np.zeros(n_grid**4)
                for T in D:
                    if len(T) < 1:
                        continue
                    start = point_to_grid(T[0])
                    end = point_to_grid(T[-1])
                    trip_counts[start * n_grid**2 + end] += 1
                return trip_counts / np.sum(trip_counts)
            
            original_trip_distribution = get_trip_distribution(original_D)
            synthetic_trip_distribution = get_trip_distribution(synthetic_D)

            return original_trip_distribution, synthetic_trip_distribution
        
        ori_dist, syn_dist = [], []
        for i in range(len(self.D)):
            ori, syn = calculate_te(self.D[i], self.D_processed_coord[i])
            ori_dist.extend(ori)
            syn_dist.extend(syn)
        
        te_score = js_divergence(ori_dist, syn_dist)

        return te_score


def plot_all_metrics(
        epsilon_list=[0.1, 0.2, 0.3, 0.4], 
        d_list=[2, 3, 4, 5, 6]
    ):
    fig, axes = plt.subplots(1, 5, figsize=(25, 5))
    all_metrics = {d: {'RE': [], 'FPS': [], 'KT': [], 'DE': [], 'TE': []} for d in d_list}
    
    for d in d_list:
        for epsilon in epsilon_list:
            evaluator = Evaluate(epsilon=epsilon, d=d)
            
            re = evaluator.RE()
            all_metrics[d]['RE'].append(re)
            
            fps, kt = evaluator.FPS_KT()
            all_metrics[d]['FPS'].append(fps)
            all_metrics[d]['KT'].append(kt)
            
            de = evaluator.DE()
            all_metrics[d]['DE'].append(de)

            te = evaluator.TE()
            all_metrics[d]['TE'].append(te)
    
    for i, (metric_name, ax) in enumerate(zip(['RE', 'FPS', 'KT', 'TE', 'DE'], axes)):
        for d in d_list:
            ax.plot(epsilon_list, all_metrics[d][metric_name], label=f'd={d}', marker='o')
        
        ax.set_xlabel(r'$\epsilon$')
        ax.set_title(f'{metric_name}-$\\epsilon$')
        ax.legend()
        ax.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    epsilon_list = [0.1, 0.2, 0.3, 0.4]
    d_list = [6]
    plot_all_metrics(epsilon_list=epsilon_list, d_list=d_list)
