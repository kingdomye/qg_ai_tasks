//
//  main.cpp
//  vector容器
//
//  Created by 陈英锐 on 2024/9/28.
//

#include <iostream>
#include <vector>

int main() {
    std::vector<int> myvector(5, 10);
    myvector.push_back(99);
    std::cout << myvector.size() << std::endl;
    
    for (int item : myvector) {
        std::cout << item << std::endl;
    }
    
    return 0;
}
