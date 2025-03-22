//
//  main.cpp
//  字符串算法
//
//  Created by 陈英锐 on 2024/10/14.
//

#include <iostream>

using namespace std;

//括号匹配问题
bool isProperlyNested(string expression)
{
    int cnt = 0;
    for (char s : expression) {
        if (s == '(') {
            cnt++;
        } else if (s == ')') {
            cnt--;
            if (cnt < 0) {
                return false;
            }
        }
    }
    
    return true;
}

int main() {
    string myStr = "))((";
    cout << isProperlyNested(myStr) << endl;
    
    return 0;
}
