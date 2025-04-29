'''
----------------------------------------------------
# file:         visualize.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  动态显示轨迹图，不带差分隐私版
----------------------------------------------------
'''

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import matplotlib.cm as cm
from itertools import count

def visualize_car_paths(data, time_interval=1.0):
    # 预处理数据，保留路径结构
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
    
    # 找到最大时间
    max_time = max([point["time"] for car in cars for path in car["paths"] for point in path])
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 自动确定坐标范围
    all_coords = [point["coords"] for car in cars for path in car["paths"] for point in path]
    x_coords = [c[0] for c in all_coords]
    y_coords = [c[1] for c in all_coords]
    ax.set_xlim(min(x_coords)-5, max(x_coords)+5)
    ax.set_ylim(min(y_coords)-5, max(y_coords)+5)
    
    ax.set_title(f"Vehicle Trajectories (Time Interval: {time_interval}s)")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    
    # 为每辆车创建颜色和绘图元素
    colors = cm.rainbow(np.linspace(0, 1, len(cars)))
    car_elements = []
    
    for i, car in enumerate(cars):
        # 为每条路径创建线
        path_lines = []
        for path in car["paths"]:
            line, = ax.plot([], [], '-', color=colors[i], alpha=0.7, lw=2)
            path_lines.append(line)
        
        # 当前位置标记
        current_pos = ax.scatter([], [], color=colors[i], s=120, 
                                marker='o', edgecolor='white', 
                                label=f'Car {car["car_num"]}')
        
        car_elements.append({
            "path_lines": path_lines,
            "current_pos": current_pos,
            "paths": car["paths"]
        })
    
    # 添加图例
    ax.legend()
    
    # 时间文本
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)
    
    # 动画更新函数
    def update(frame_time):
        time_text.set_text(f'Time: {frame_time:.1f}s')
        
        updated_artists = [time_text]
        
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
        
        return updated_artists
    
    # 创建动画
    frame_times = np.arange(0, max_time + time_interval, time_interval)
    ani = FuncAnimation(fig, update, frames=frame_times, 
                       interval=100, blit=True, repeat=True)
    
    plt.tight_layout()
    plt.show()
    return ani

# 使用示例
import json
with open('./trajectory.json', 'r') as f:
    data = json.load(f)
visualize_car_paths(data, time_interval=2.0)