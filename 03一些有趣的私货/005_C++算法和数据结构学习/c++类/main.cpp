//
//  main.cpp
//  c++类
//
//  Created by 陈英锐 on 2024/9/25.
//

#include <iostream>
#include <string>

class Book
{
public:
    Book(std::string name, int val);
    ~Book(void);
    
private:
    std::string name;
    int price;
};

Book::Book(std::string name, int val): name(name), price(val)
{
    std::cout << "book is being created:" << name << std::endl;
}

Book::~Book(void)
{
    std::cout << "being deleted" << std::endl;
}

int main() {
    Book book1("aaa", 10);

    return 0;
}
