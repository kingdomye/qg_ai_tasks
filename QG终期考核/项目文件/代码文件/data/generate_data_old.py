'''
----------------------------------------------------
# file:         generate_data_old.py
# author:       Yingrui Chen
# date:         2025/4/25
# description:  生成轨迹数据
----------------------------------------------------
'''

import random
import json
import time
from datetime import datetime, timedelta

def generate_trajectory_data(lat_range, lon_range, time_range, num_trajectories, output_file=None):
    """
    生成轨迹数据
    
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
    
    trajectories = []
    
    for car_num in range(1, num_trajectories + 1):
        # 随机生成车辆速度 (0.3-0.7)
        speed = round(random.uniform(0.3, 0.7), 1)
        
        # 随机生成路径数量 (1-5)
        num_paths = random.randint(5, 10)
        paths = []
        
        for _ in range(num_paths):
            # 随机生成路径长度 (2-10个点)
            path_length = random.randint(10, 20)
            path = []
            
            # 随机生成起始时间戳
            timestamp = random.uniform(start_timestamp, end_timestamp)
            
            # 生成路径点
            relative_time = 0.0
            for i in range(path_length):
                # 随机生成节点名称 (1-40)
                node_name = random.randint(1, 30)
                
                # 随机生成坐标
                lat = round(random.uniform(min_lat, max_lat), 3)
                lon = round(random.uniform(min_lon, max_lon), 3)
                
                # 随机生成旅行时间 (1-20秒)
                if i == 0:
                    travel_time = round(random.uniform(1, 5), 6)
                else:
                    travel_time = round(random.uniform(1, 20), 6)
                
                relative_time += travel_time
                
                path.append({
                    "node_name": node_name,
                    "coords": [lat, lon],
                    "relative_time": round(relative_time, 6),
                    "travel_time": round(travel_time, 6),
                    "timestamp": round(timestamp + relative_time, 6)
                })
            
            paths.append(path)
        
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

# 使用示例
if __name__ == "__main__":
    # 设置参数
    lat_range = (10.0, 150.0)  # 纬度范围
    lon_range = (1.0, 150.0)    # 经度范围
    time_range = ('2024-01-01', '2024-01-31')  # 时间范围
    num_trajectories =20  # 轨迹数量
    
    # 生成轨迹数据
    trajectories = generate_trajectory_data(
        lat_range=lat_range,
        lon_range=lon_range,
        time_range=time_range,
        num_trajectories=num_trajectories,
        output_file="test.json"  # 可选，不提供则返回数据
    )
    
    # 如果未指定输出文件，打印前两条轨迹
    if trajectories:
        print(json.dumps(trajectories[:2], indent=4))