//
//  main.cpp
//  简单图
//
//  Created by 陈英锐 on 2024/10/14.
//

#include <iostream>
using namespace std;

//网络节点类
class Node
{
public:
    string name;
    bool visited;
    unordered_map<Node*, Node*> Links;
    
    Node(string name):name(name), visited(false){}
    
    void addLink(Node* next);
    void depthFirstTraverse();
    void breadthFirstTraverse();
    void isConnected();
};

//有向图添加边
void Node::addLink(Node* next)
{
    this->Links[next] = next;
}

//有向图深度优先遍历
void Node::depthFirstTraverse()
{
    cout << this->name << endl;
    this->visited = true;
    
    for (auto &link : Links) {
        if (!link.second->visited) {
            link.second->depthFirstTraverse();
        }
    }
}

//有向图广度优先遍历
void Node::breadthFirstTraverse()
{
    queue<Node*> myQueue;
    myQueue.push(this);
    this->visited = true;
    
    while (!myQueue.empty()) {
        for (auto &link : myQueue.front()->Links) {
            if (!link.second->visited){
                myQueue.push(link.second);
                link.second->visited = true;
            }
        }
        
        cout << myQueue.front()->name << endl;
        myQueue.pop();
    }
}

int main() {
    Node A("A");
    Node B("B");
    Node C("C");
    Node D("D");
    Node E("E");
    
    A.addLink(&E);
    A.addLink(&B);
    B.addLink(&C);
    C.addLink(&D);
    
    A.breadthFirstTraverse();

    return 0;
}
