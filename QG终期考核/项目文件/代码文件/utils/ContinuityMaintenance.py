'''
----------------------------------------------------
# file:         ContinuityMaintenance.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  时空连续性维护
----------------------------------------------------
'''

from collections import defaultdict
import numpy as np

class ContinuityMaintenance:
    def __init__(self, D_r, g_dict, g):
        self.D_r = D_r
        self.g_dict = g_dict
        self.g = g

        self.output = self.main()

    def main(self):
        '''
        :param D_r: 合成轨迹
        :param g: 网格大小
        :return: 处理完成的数据集D
        '''
        def angle_between_vectors(v1, v2):
            unit_v1 = v1 / np.linalg.norm(v1) if np.linalg.norm(v1) != 0 else v1
            unit_v2 = v2 / np.linalg.norm(v2) if np.linalg.norm(v2) != 0 else v2
            dot_product = np.dot(unit_v1, unit_v2)
            angle = np.arccos(np.clip(dot_product, -1.0, 1.0))

            return np.degrees(angle)

        def project_point_to_line(p, a, b):
            a = np.array(a)
            b = np.array(b)
            ab = b - a
            ap = p - a
            t = np.dot(ap, ab) / np.dot(ab, ab)
            t = np.clip(t, 0, 1)
            projection = a + t * ab

            center_x = (projection[0] + projection[2]) / 2
            center_y = (projection[1] + projection[3]) / 2
            result = [center_x, center_y]
            
            return result
        
        def find_grid_index(point, g_dict):
            x, y = point
            for grid_idx, cell in g_dict.items():
                x_min, y_min, x_max, y_max = cell.bounds
                if x_min <= x <= x_max and y_min <= y <= y_max:
                    return grid_idx
            return None
            
        def direction_based_processing(D):
            processed = []

            for T in D:
                if len(T) < 4:
                    processed.append(T)
                    continue

                l0, l1, l2, l3 = self.g_dict[T[-4]].bounds, self.g_dict[T[-3]].bounds, self.g_dict[T[-2]].bounds, self.g_dict[T[-1]].bounds
                    
                vec_alpha = (l1[0]-l0[0], l1[1]-l0[1])
                vec_gamma = (l3[0]-l1[0], l3[1]-l1[1])
                vec_l2 = (l2[0]-l1[0], l2[1]-l1[1])

                theta0 = angle_between_vectors(vec_alpha, vec_gamma)
                theta1 = angle_between_vectors(vec_l2, vec_gamma)

                if theta1 < theta0:
                    pass
                elif theta0 < theta1 < 90:
                    proj = project_point_to_line(l2, l1, l3)
                    proj_grid_idx = find_grid_index(proj, self.g_dict)
                    if proj_grid_idx is not None:
                        T[-2] = proj_grid_idx
                else:
                    T.pop(-2)
                processed.append(T)
                
            return processed
            
        def density_based_correction(D, grid_size):
            density_map = defaultdict(lambda: np.zeros((grid_size, grid_size)))
            start_end_counts = defaultdict(int)
                
            for traj in D:
                if len(traj) < 2:
                    continue
                        
                start, end = traj[0], traj[-1]
                key = (start, end)
                start_end_counts[key] += 1
                    
                for point in traj[1:-1]:
                    x = point % grid_size
                    y = point // grid_size
                    density_map[key][x, y] += 1
                
            processed = []
            for traj in D:
                if len(traj) < 2:
                    processed.append(traj)
                    continue
                        
                start, end = traj[0], traj[-1]
                key = (start, end)
                threshold = start_end_counts[key]
                    
                filtered_traj = [traj[0]]
                    
                for point in traj[1:-1]:
                    x = point % grid_size
                    y = point // grid_size
                        
                    if density_map[key][x, y] >= threshold:
                        filtered_traj.append(point)
                    
                filtered_traj.append(traj[-1])
                processed.append(filtered_traj)
                
            return processed
            
        D_processed = direction_based_processing(self.D_r)
        D_processed = density_based_correction(D_processed, self.g)

        return D_processed
    