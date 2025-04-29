'''
----------------------------------------------------
# file:         GridCell.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  网格类
----------------------------------------------------
'''

from matplotlib import pyplot as plt

class GridCell:
    def __init__(self, bounds, resolution=0):
        self.bounds = bounds            # 网格边界
        self.resolution = resolution    # 网格分辨率
        self.children = []              # 子网格列表
        self.trajectory_points = []     # 网格内轨迹点

    def is_leaf(self):
        return len(self.children) == 0
    
    # 将当前网格划分为 d x d子网格
    def split(self, d):
        min_x, min_y, max_x, max_y = self.bounds
        dx = (max_x - min_x) / d
        dy = (max_y - min_y) / d

        for i in range(d):
            for j in range(d):
                child_bounds = [
                    min_x + i * dx,
                    min_y + j * dy,
                    min_x + (i + 1) * dx,
                    min_y + (j + 1) * dy
                ]
                self.children.append(GridCell(child_bounds, self.resolution + 1))

    def show(self, cell):
        x = [cell.bounds[0], cell.bounds[2], cell.bounds[2], cell.bounds[0], cell.bounds[0]]
        y = [cell.bounds[1], cell.bounds[1], cell.bounds[3], cell.bounds[3], cell.bounds[1]]
        plt.plot(x, y, color='r', linewidth=0.5, alpha=0.5)
        for child in cell.children:
            self.show(child)

    def contains(self, point):
        return (self.bounds[0]-(1e-3) <= point[0] <= self.bounds[2]+(1e-3)) and \
                (self.bounds[1]-(1e-3) <= point[1] <= self.bounds[3]+(1e-3))
    
    def get_all_leaf_cells(self):
        if self.is_leaf():
            return [self]
        leaves = []
        for child in self.children:
            leaves.extend(child.get_all_leaf_cells())
        return leaves
    
    def map_point_to_cell(self, point):
        if self.is_leaf():
            return self
        for child in self.children:
            if child.contains(point):
                return child.map_point_to_cell(point)
        return self


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    bounds = [25, 15, 35, 30]
    cell = GridCell(bounds)
    # 绘制正方形边框
    plt.plot([25, 35, 35, 25, 25], [15, 15, 30, 30, 15], color='r')
    cell.split(3)
    cell.show(cell)
    plt.show()
