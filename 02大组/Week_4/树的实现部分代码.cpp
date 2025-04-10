//
//  main.cpp
//  树
//
//  Created by 陈英锐 on 2024/9/27.
//

#include <iostream>
#include <cstdlib>
#include <ctime>
//*********************
//***** 常规二叉树 ******
//*********************

//常规二叉树节点类
class BinaryNode
{
public:
    int data;
    
    BinaryNode* leftChild;
    BinaryNode* rightChild;
    
    BinaryNode():data(NULL), leftChild(NULL), rightChild(NULL){}
    BinaryNode(int data):data(data), leftChild(NULL), rightChild(NULL){}
};

//用于返回查找参数的结构体
struct returnParams
{
    BinaryNode* parentNode;         //当前节点的父节点
    BinaryNode* currentNode;        //当前节点
    int direction;                  //direction方向参数：0为左子树，1为右子树
};

//二叉树类
class BinaryTree
{
public:
    BinaryNode* root;
    
    void addNode(int value, BinaryNode* node);
    returnParams findNode(int target, BinaryNode* node, returnParams& params);
    void deleteNode(int target);
    
    void traversePreOrder(BinaryNode* node);
    void traverseInOrder(BinaryNode* node);
    void traversePostOrder(BinaryNode* node);
    void traverseDepthFirst(BinaryNode* node);
    
    BinaryNode* findLcaSortedTree(int value1, int value2, BinaryNode* curNode);
    
    BinaryTree():root(NULL){}
};

//有序二叉树插入节点
void BinaryTree::addNode(int value, BinaryNode* node)
{
    BinaryNode* newNode = new BinaryNode(value);
    
    if (this->root == NULL) {
        this->root = newNode;
    } else {
        if (newNode->data < node->data) {
            if (node->leftChild == NULL) {
                node->leftChild = newNode;
            } else {
                addNode(value, node->leftChild);
            }
        } else {
            if (node->rightChild == NULL) {
                node->rightChild = newNode;
            } else {
                addNode(value, node->rightChild);
            }
        }
    }
}

//有序二叉树查找节点
returnParams BinaryTree::findNode(int target, BinaryNode* node, returnParams& params)
{
    params.currentNode = node;
    if (node->data == target) {
        return params;
    }
    
    params.parentNode = node;
    if (target < node->data) {
        //目标值小于当前节点值，递归插入左子树
        params.direction = 0;
        if (node->leftChild == NULL) {
            params.currentNode = NULL;
            return params;
        } else {
            return findNode(target, node->leftChild, params);
        }
    } else {
        //目标值大于等于当前节点值，递归插入右子树
        params.direction = 1;
        if (node->rightChild == NULL) {
            params.currentNode = NULL;
            return params;
        } else {
            return findNode(target, node->rightChild, params);
        }
    }
    
    return params;
}

//有序二叉树删除节点
void BinaryTree::deleteNode(int target)
{
    returnParams inputParams;
    returnParams findParams = this->findNode(target, this->root, inputParams);
    
    if (findParams.currentNode != NULL) {
        
        //情况1、目标节点为叶子节点：直接删除
        if (findParams.currentNode->leftChild == NULL && findParams.currentNode->rightChild == NULL) {
            if (findParams.direction == 0) {
                findParams.parentNode->leftChild = NULL;
            } else {
                findParams.parentNode->rightChild = NULL;
            }
        }
        
        //情况2、目标节点有1个子节点:子节点替换父节点
        //基本思路：parent.direction = current.child
        else if ((findParams.currentNode->leftChild == NULL && findParams.currentNode->rightChild != NULL) || (findParams.currentNode->leftChild != NULL && findParams.currentNode->rightChild == NULL)) {
            
            if (findParams.direction == 0) {
                findParams.parentNode->leftChild = (findParams.currentNode->leftChild == NULL) ? findParams.currentNode->rightChild : findParams.currentNode->leftChild;
            } else {
                findParams.parentNode->rightChild = (findParams.currentNode->leftChild == NULL) ? findParams.currentNode->rightChild : findParams.currentNode->leftChild;
            }
        }
        
        //情况3、目标节点有2个子节点:左子节点替换父节点
        else {
            //子情况1、目标节点的左子节点没有右子节点:左子节点直接替换目标节点
            if (findParams.currentNode->leftChild->rightChild == NULL) {
                if (findParams.direction == 0) {
                    findParams.parentNode->leftChild = findParams.currentNode->leftChild;
                } else {
                    findParams.parentNode->rightChild = findParams.currentNode->leftChild;
                }
            }
            
            //子情况2、目标节点的左子节点还有右子节点：向下搜索到树的最右节点
            //若最右节点没有左子节点，直接替换；最右节点有左子节点，则目标节点替换为最右节点， 左子节点替换为最右节点
            else {
                BinaryNode* curNode = findParams.currentNode->leftChild;
                while (curNode->rightChild != NULL) {
                    curNode = curNode->rightChild;
                }
                
                findParams.currentNode->data = curNode->data;
                if (curNode->leftChild == NULL) {
                    curNode = NULL;
                } else {
                    curNode->data = curNode->leftChild->data;
                    curNode->leftChild = NULL;
                }
            }
            
        }
    } else {
        std::cout << "Not find the target node!" << std::endl;
    }
    return;
}

//二叉树前序遍历
void BinaryTree::traversePreOrder(BinaryNode* node)
{
    std::cout << node->data << std::endl;
    
    if (node->leftChild != NULL) {
        traversePreOrder(node->leftChild);
    }
    
    if (node->rightChild != NULL) {
        traversePreOrder(node->rightChild);
    }
}

//二叉树中序遍历
void BinaryTree::traverseInOrder(BinaryNode* node)
{
    if (node->leftChild != NULL) {
        traverseInOrder(node->leftChild);
    }
    
    std::cout << node->data << std::endl;
    
    if (node->rightChild != NULL) {
        traverseInOrder(node->rightChild);
    }
}

//二叉树后序遍历
void BinaryTree::traversePostOrder(BinaryNode* node)
{
    if (node->leftChild != NULL) {
        traversePostOrder(node->leftChild);
    }
    
    if (node->rightChild != NULL) {
        traversePostOrder(node->rightChild);
    }
    
    std::cout << node->data << std::endl;
}

//二叉树层序遍历
void BinaryTree::traverseDepthFirst(BinaryNode* node)
{
    std::queue<BinaryNode*> myqueue;
    myqueue.push(node);
    
    while (!myqueue.empty()) {
        if (myqueue.front()->leftChild != NULL) {
            myqueue.push(myqueue.front()->leftChild);
        }
        if (myqueue.front()->rightChild != NULL) {
            myqueue.push(myqueue.front()->rightChild);
        }
        
        std::cout << myqueue.front()->data << std::endl;
        myqueue.pop();
    }
}

//有序树查找最小共同祖先(也可以递归实现）
BinaryNode* BinaryTree::findLcaSortedTree(int value1, int value2, BinaryNode* curNode)
{
    while (!(value1 <= curNode->data && curNode->data <= value2)) {
        curNode = (curNode->data < value1 && curNode->data < value2) ? curNode->rightChild : curNode->leftChild;
    }
    return curNode;
}

//生成随机有序二叉树
BinaryTree createRandomSortBinaryTree(int size)
{
    BinaryTree resTree;
    srand(static_cast<unsigned int>(time(0)));
    for (int i = 0; i < size; i++) {
        resTree.addNode(rand() % 100 + 1, resTree.root);
    }
    
    return resTree;
}


//*********************
//****** 区间树 ********
//*********************

//区间struct
struct interval
{
    int low, high;
};

//区间树节点类
class ITNode
{
public:
    interval* i;            //区间
    int max;                //最大值
    ITNode* left;           //指向左子节点区间
    ITNode* right;          //指向右子节点区间
    
    ITNode(interval i):i(new interval(i)), max(i.high), left(nullptr), right(nullptr){}
};

//区间树类
class IntervalTree
{
public:
    ITNode* root;
    
    IntervalTree():root(nullptr){}
    
    ITNode* insertNode(ITNode* root, interval i);
};

ITNode* insertNode(ITNode* root, interval i)
{
    if (root == nullptr) {
        return new ITNode(i);
    }
    
    int low = root->i->low;
    if (i.low < low) {
        root->left = insertNode(root->left, i);
    } else {
        root->right = insertNode(root->right, i);
    }
    root->max = std::max(i.high, root->max);
    
    return root;
}

//*********************
//***** AVL平衡树 ******
//*********************

//平衡树节点类
class AVLTreeNode
{
public:
    int data;
    int depth;
    
    AVLTreeNode* leftChild;
    AVLTreeNode* rightChild;
    
    AVLTreeNode():data(NULL), depth(NULL), leftChild(nullptr), rightChild(nullptr){}
    AVLTreeNode(int data):data(data), depth(NULL), leftChild(nullptr), rightChild(nullptr){}
};

//平衡树类
class AVLTree
{
public:
    AVLTreeNode* root;
    int balanceCase;
    
    AVLTree():root(nullptr), balanceCase(0){}
    
    void addNode(int data, AVLTreeNode* curNode, int depth);
    AVLTree* createRandomAVLTree(int size);
    int caculateBalanceCase(AVLTree* curNode);
};

void AVLTree::addNode(int data, AVLTreeNode *curNode, int depth)
{
    AVLTreeNode* newNode = new AVLTreeNode(data);
    newNode->depth = depth;
    
    if (this->root == nullptr) {
        this->root = newNode;
    } else {
        if (data < curNode->data) {
            if (curNode->leftChild == nullptr) {
                newNode->depth++;
                curNode->leftChild = newNode;
            } else {
                this->addNode(data, curNode->leftChild, ++depth);
            }
        } else {
            if (curNode->rightChild == nullptr) {
                newNode->depth++;
                curNode->rightChild = newNode;
            } else {
                this->addNode(data, curNode->rightChild, ++depth);
            }
        }
    }
}

AVLTree* AVLTree::createRandomAVLTree(int size)
{
    srand(static_cast<unsigned int>(time(0)));
    AVLTree* result = new AVLTree;
    
    for (int i = 0; i < size; i++) {
        result->addNode(rand() % 100 + 1, result->root, 0);
    }
    
    return result;
}

int AVLTree::caculateBalanceCase(AVLTree* curNode)
{
    int result = 0;
    
    
    return result;
}

int main() {
    AVLTree* myAVLTree = new AVLTree;
    myAVLTree = myAVLTree->createRandomAVLTree(20);
    std::cout << myAVLTree->root->leftChild->depth << std::endl;

    return 0;
}
