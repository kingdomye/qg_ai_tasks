'''
----------------------------------------------------
# file:         generate_data_improve.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  生成更符合现实生活分布的轨迹数据
----------------------------------------------------
'''

import random
import json
import time
import math
from datetime import datetime, timedelta
import numpy as np

def generate_trajectory_data(lat_range, lon_range, time_range, num_trajectories, output_file=None):
    """
    生成更符合现实生活分布的轨迹数据
    
    Args:
        lat_range: 纬度范围 (min_lat, max_lat)
        lon_range: 经度范围 (min_lon, max_lon)
        time_range: 时间范围 (start_date, end_date) 格式为 'yyyy-mm-dd'
        num_trajectories: 要生成的轨迹数量
        output_file: 输出文件路径(可选)，如果不提供则返回数据
    
    Returns:
        如果output_file为None，返回生成的轨迹数据，否则保存到文件
    """
    min_lat, max_lat = lat_range
    min_lon, max_lon = lon_range
    start_date, end_date = time_range
    
    # 将日期字符串转换为时间戳
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    start_timestamp = time.mktime(start_dt.timetuple())
    end_timestamp = time.mktime(end_dt.timetuple())
    
    # 创建热点区域（市中心、商业区等）
    hotspots_w1 = random.uniform(0, 1)
    hotspots_w2 = random.uniform(0, 1)
    hotspots_w3 = random.uniform(0, 1)
    hotspots_w4 = random.uniform(0, 1)
    hotspots = [
        {"center": (np.mean(lat_range), np.mean(lon_range)), "radius": 0.2, "weight": 0.5},
        {"center": (min_lat + hotspots_w1*(max_lat-min_lat), min_lon + hotspots_w2*(max_lon-min_lon)), "radius": 0.15, "weight": 0.3}
    ]
    
    # 主要道路方向（模拟城市网格）
    main_directions = [0, math.pi/4, math.pi/2, 3*math.pi/4]
    
    trajectories = []
    
    for car_num in range(1, num_trajectories + 1):
        # 随机生成车辆速度 (0.3-0.7)
        speed = round(random.uniform(0.3, 0.7), 1)
        
        # 随机生成路径数量 (1-5)
        num_paths = random.randint(5, 10)
        paths = []
        
        # 随机选择起始点（更可能在热点区域）
        current_lat, current_lon = _get_weighted_random_point(lat_range, lon_range, hotspots)
        
        for _ in range(num_paths):
            # 随机生成路径长度 (10-20个点)
            path_length = random.randint(40, 60)
            path = []
            
            # 随机生成起始时间戳
            timestamp = random.uniform(start_timestamp, end_timestamp)
            
            # 选择主要移动方向
            direction = random.choice(main_directions)
            # 添加一些随机偏移
            direction += random.uniform(-math.pi/8, math.pi/8)
            
            # 生成路径点
            relative_time = 0.0
            for i in range(path_length):
                # 随机生成节点名称 (1-40)
                node_name = random.randint(1, 30)
                
                # 模拟车辆在道路上的移动
                if i > 0:
                    # 80%的概率沿着道路方向移动
                    if random.random() < 0.8:
                        step_size = 0.02 * speed  # 调整步长
                        current_lat += step_size * math.cos(direction)
                        current_lon += step_size * math.sin(direction)
                        
                        # 确保不超出范围
                        current_lat = max(min_lat, min(max_lat, current_lat))
                        current_lon = max(min_lon, min(max_lon, current_lon))
                    else:
                        # 20%的概率改变方向（模拟转弯）
                        direction = random.choice(main_directions)
                        direction += random.uniform(-math.pi/8, math.pi/8)
                
                # 10%的概率模拟停留（红绿灯、停车等）
                if random.random() < 0.1:
                    travel_time = round(random.uniform(5, 30), 6)  # 较长停留时间
                else:
                    if i == 0:
                        travel_time = round(random.uniform(1, 5), 6)
                    else:
                        travel_time = round(random.uniform(1, 10), 6)
                
                relative_time += travel_time
                
                path.append({
                    "node_name": node_name,
                    "coords": [round(current_lat, 6), round(current_lon, 6)],
                    "relative_time": round(relative_time, 6),
                    "travel_time": round(travel_time, 6),
                    "timestamp": round(timestamp + relative_time, 6)
                })
            
            paths.append(path)
            
            # 为下一条路径随机选择新的起点（可能在热点区域）
            current_lat, current_lon = _get_weighted_random_point(lat_range, lon_range, hotspots)
        
        trajectories.append({
            "car_num": car_num,
            "speed": speed,
            "paths": paths
        })
    
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(trajectories, f, indent=4)
        print(f"轨迹数据已保存到 {output_file}")
    else:
        return trajectories

def _get_weighted_random_point(lat_range, lon_range, hotspots):
    """根据热点区域权重随机选择点"""
    min_lat, max_lat = lat_range
    min_lon, max_lon = lon_range
    
    # 决定是否在热点区域生成点
    if random.random() < 0.7:  # 70%的概率在热点区域
        hotspot = random.choices(
            hotspots, 
            weights=[h['weight'] for h in hotspots],
            k=1
        )[0]
        
        center_lat, center_lon = hotspot['center']
        radius = hotspot['radius']
        
        # 在热点区域内生成随机点
        angle = random.uniform(0, 2*math.pi)
        distance = random.uniform(0, radius)
        
        lat = center_lat + distance * math.cos(angle)
        lon = center_lon + distance * math.sin(angle)
        
        # 确保不超出范围
        lat = max(min_lat, min(max_lat, lat))
        lon = max(min_lon, min(max_lon, lon))
        
        return lat, lon
    else:
        # 在非热点区域随机生成
        return random.uniform(min_lat, max_lat), random.uniform(min_lon, max_lon)

# 使用示例
if __name__ == "__main__":
    # 设置参数
    lat_range = (30.0, 31.0)  # 更合理的纬度范围（约100公里）
    lon_range = (120.0, 121.0)  # 更合理的经度范围（约100公里）
    time_range = ('2024-01-01', '2024-01-31')  # 时间范围
    num_trajectories = 20  # 轨迹数量
    
    # 生成轨迹数据
    trajectories = generate_trajectory_data(
        lat_range=lat_range,
        lon_range=lon_range,
        time_range=time_range,
        num_trajectories=num_trajectories,
        output_file="realistic_trajectories.json"  # 可选，不提供则返回数据
    )
    
    # 如果未指定输出文件，打印前两条轨迹
    if trajectories:
        print(json.dumps(trajectories[:2], indent=4))