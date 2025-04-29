'''
----------------------------------------------------
# file:         visualize.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  带差分隐私的动态轨迹可视化动画
----------------------------------------------------
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
from itertools import count

def visualize_car_paths_with_processed(data, D_p_c, time_interval=1.0, G=None):
    # 预处理原始数据，保留路径结构
    cars = []
    for car_data in data:
        car_num = car_data["car_num"]
        paths = []
        
        # 对每条路径单独处理
        for path in car_data["paths"]:
            path_points = []
            cumulative_time = 0
            for point in path:
                # 计算绝对时间（假设timestamp是起始时间）
                abs_time = point["relative_time"]
                path_points.append({
                    "coords": point["coords"],
                    "time": abs_time,
                    "node_name": point["node_name"]
                })
            paths.append(path_points)
        
        cars.append({
            "car_num": car_num,
            "paths": paths
        })
    
    # 预处理D_p_c数据，假设每条处理后的轨迹对应原始轨迹的时间点
    processed_cars = []
    for i, car_data in enumerate(D_p_c):
        car_num = cars[i]["car_num"] if i < len(cars) else f"P_{i}"  # 保持与原始数据相同的车辆编号
        paths = []
        
        # 假设处理后的轨迹点与原始轨迹点时间一一对应
        for path_idx, path in enumerate(car_data):
            path_points = []
            # 获取原始轨迹的时间点
            original_times = [p["time"] for p in cars[i]["paths"][path_idx]] if (i < len(cars) and path_idx < len(cars[i]["paths"])) else np.linspace(0, 10, len(path))
            
            for point_idx, point in enumerate(path):
                # 使用原始轨迹的时间或均匀分布的时间
                time = original_times[point_idx] if point_idx < len(original_times) else point_idx * time_interval
                path_points.append({
                    "coords": point,
                    "time": time,
                    "node_name": f"P_{point_idx}"
                })
            paths.append(path_points)
        
        processed_cars.append({
            "car_num": car_num,
            "paths": paths
        })
    
    # 找到最大时间（原始和处理后的）
    max_time_original = max([point["time"] for car in cars for path in car["paths"] for point in path], default=0)
    max_time_processed = max([point["time"] for car in processed_cars for path in car["paths"] for point in path], default=0)
    max_time = max(max_time_original, max_time_processed)
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 自动确定坐标范围（包含原始和处理后的数据）
    all_coords = [point["coords"] for car in cars for path in car["paths"] for point in path] + \
                 [point for car in processed_cars for path in car["paths"] for point in path]

    x_coords = []
    y_coords = []
    for c in all_coords:
        if type(c) is dict:
            c = c['coords']
            c = [c[0], c[1]]
        x_coords.append(c[0])
        y_coords.append(c[1])
    # x_coords = [c[0] for c in all_coords]
    # y_coords = [c[1] for c in all_coords]
    ax.set_xlim(min(x_coords)-5, max(x_coords)+5)
    ax.set_ylim(min(y_coords)-5, max(y_coords)+5)
    
    ax.set_title(f"Vehicle Trajectories (Original and Processed) (Time Interval: {time_interval}s)")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    
    # 为每辆车创建颜色和绘图元素（原始数据）
    colors = cm.rainbow(np.linspace(0, 1, max(len(cars), len(processed_cars))))
    car_elements = []
    processed_car_elements = []
    
    # 原始数据元素
    for i, car in enumerate(cars):
        # 为每条路径创建线
        path_lines = []
        for path in car["paths"]:
            line, = ax.plot([], [], '-', color=colors[i], alpha=0.7, lw=2)
            path_lines.append(line)
        
        # 当前位置标记
        current_pos = ax.scatter([], [], color=colors[i], s=120, 
                                marker='o', edgecolor='white', 
                                label=f'Car {car["car_num"]} (Original)')
        
        car_elements.append({
            "path_lines": path_lines,
            "current_pos": current_pos,
            "paths": car["paths"]
        })
    
    # 处理后数据元素（使用相同颜色但不同样式）
    # for i, car in enumerate(processed_cars):
    #     # 为每条路径创建虚线
    #     path_lines = []
    #     for path in car["paths"]:
    #         line, = ax.plot([], [], '--', color=colors[i], alpha=0.7, lw=2)
    #         path_lines.append(line)
        
    #     # 当前位置标记（使用不同形状）
    #     current_pos = ax.scatter([], [], color=colors[i], s=120, 
    #                             marker='s', edgecolor='white', 
    #                             label=f'Car {car["car_num"]} (Processed)')
        
    #     processed_car_elements.append({
    #         "path_lines": path_lines,
    #         "current_pos": current_pos,
    #         "paths": car["paths"]
    #     })
    # 处理后的元素绘制散点图
    for car in processed_cars:
        for path in car["paths"]:
            for point in path:
                ax.scatter(point["coords"][0], point["coords"][1], color=colors[i], s=100, alpha=0.5, marker='s')

    
    # 添加图例
    ax.legend()
    
    # 时间文本
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
    
    # 动画更新函数
    def update(frame_time):
        time_text.set_text(f'Time: {frame_time:.1f}s')
        
        updated_artists = [time_text]
        
        # 更新原始数据
        for elements in car_elements:
            # 处理每条路径
            for path_idx, path in enumerate(elements["paths"]):
                line = elements["path_lines"][path_idx]
                
                # 获取当前时间之前的点
                visible_points = [p for p in path if p["time"] <= frame_time]
                
                if visible_points:
                    x = [p["coords"][0] for p in visible_points]
                    y = [p["coords"][1] for p in visible_points]
                    line.set_data(x, y)
                    updated_artists.append(line)
            
            # 更新当前位置（所有路径中最新的点）
            all_points = [p for path in elements["paths"] for p in path if p["time"] <= frame_time]
            if all_points:
                latest_point = max(all_points, key=lambda x: x["time"])
                elements["current_pos"].set_offsets([latest_point["coords"]])
                updated_artists.append(elements["current_pos"])
        
        # 更新处理后数据
        for elements in processed_car_elements:
            # 处理每条路径
            for path_idx, path in enumerate(elements["paths"]):
                line = elements["path_lines"][path_idx]
                
                # 获取当前时间之前的点
                visible_points = [p for p in path if p["time"] <= frame_time]
                
                if visible_points:
                    x = [p["coords"][0] for p in visible_points]
                    y = [p["coords"][1] for p in visible_points]
                    line.set_data(x, y)
                    updated_artists.append(line)
            
            # 更新当前位置（所有路径中最新的点）
            all_points = [p for path in elements["paths"] for p in path if p["time"] <= frame_time]
            if all_points:
                latest_point = max(all_points, key=lambda x: x["time"])
                elements["current_pos"].set_offsets([latest_point["coords"]])
                updated_artists.append(elements["current_pos"])
        
        return updated_artists
    
    # 创建动画
    frame_times = np.arange(0, max_time + time_interval, time_interval)
    ani = FuncAnimation(fig, update, frames=frame_times, 
                       interval=100, blit=True, repeat=True)
    
    G.show(G)
    plt.tight_layout()
    plt.show()
    return ani

# 使用示例
import json
from DataLayer import Datalayer  # 假设Datalayer类在Datalayer.py中

# 加载原始数据
with open('../data/trajectory.json', 'r') as f:
    data = json.load(f)

# 获取处理后的数据
datalayer = Datalayer('../data/trajectory.json')
D_p, D_p_c, G = datalayer.process(epsilon=2, d=2, rho=2)

# 可视化原始和处理后的轨迹
visualize_car_paths_with_processed(data, D_p_c, time_interval=2.0, G=G)