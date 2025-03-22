//
//  main.cpp
//  数组探路搜索最大值
//
//  Created by 陈英锐 on 2024/10/5.
//

#include <iostream>
#include <ctime>
#include <cstdlib>

std::vector<std::vector<int>> createVector(int size)
{
    std::vector<std::vector<int>> result(size, std::vector<int> (size, 0));
    
    return result;
}

std::vector<std::vector<int>> createRandomVector(int size)
{
    std::vector<std::vector<int>> result(size, std::vector<int> (size, 0));
    srand(static_cast<unsigned int>(time(0)));
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            result[i][j] = rand() % 10 + 1;
        }
    }
    
    return result;
}

void printVector(std::vector<std::vector<int>> vec)
{
    for (std::vector<int> vector : vec) {
        for (int item : vector) {
            std::cout << item << " ";
        }
        std::cout << std::endl;
    }
}

bool findPath(int current_x, int current_y, std::vector<std::vector<int>> &map, int move_nums)
{
    if (current_x < 0 || current_y < 0 || current_x > 3 || current_y > 3) {
        return false;
    }
    
    if (move_nums == map.size() * map[0].size()) {
        map[current_x][current_y] = move_nums;
        printVector(map);
        return true;
    }
    
    std::vector<int> dx = {-1, 0, 0, 1};
    std::vector<int> dy = {0, -1, 1, 0};
    for (int i = 0; i < 4; i++) {
        if (!(current_x + dx[i] < 0 || current_y + dy[i] < 0 || current_x + dx[i] > 3 || current_y + dy[i] > 3)) {
            if (map[current_x + dx[i]][current_y + dy[i]] == 0) {
                map[current_x][current_y] = move_nums;
                if (findPath(current_x + dx[i], current_y + dy[i], map, move_nums + 1)) {
                    return true;
                }
                map[current_x][current_y] = 0;
            }
        }
    }
    
    return false;
}

bool findMaxNumPath(int current_x, int current_y, std::vector<std::vector<int>> &map, int &sum, int &max_sum, std::vector<std::pair<int, int>> &path)
{
    //当前位置越界，返回false
    if (current_x < 0 || current_y < 0 || current_x >= map.size() || current_y >= map[0].size()) {
        return false;
    }
    
    //到达终点，返回true，计算最大值
    if (current_x == map.size() - 1 && current_y == map[0].size() - 1) {
        sum += map[current_x][current_y];
        path.push_back({current_x, current_y});
        
        std::cout << "current_sum:" << sum << std::endl;
        max_sum = std::max(max_sum, sum);
        if (sum != max_sum) {
            path.pop_back();
        }
        sum -= map[current_x][current_y];
        
        printVector(map);
        std::cout << std::endl;
        return true;
    }
    
    //递归探路
    int temp = map[current_x][current_y];
    
    sum += temp;
    path.push_back({current_x, current_y});
    
    bool a = findMaxNumPath(current_x, current_y + 1, map, sum, max_sum, path);
    bool b = findMaxNumPath(current_x + 1, current_y, map, sum, max_sum, path);
    
    map[current_x][current_y] = temp;
    sum -= temp;
    
    return a || b;
}

int main() {
    std::vector<std::vector<int>> myVec = createRandomVector(3);
    int sum = 0;
    int max_sum = 0;
    std::vector<std::pair<int, int>> path;
    
    findMaxNumPath(0, 0, myVec, sum, max_sum, path);
    
    std::cout << "The final max num = " << max_sum << std::endl;
    
    std::cout << "The final path: ";
    for (std::pair<int, int> item : path) {
        std::cout << "(" << item.first << ", " << item.second << ")" << "->";
    }
    std::cout << std::endl;
    
    return 0;
}

//汉诺塔问题
//二叉树最大路问题
