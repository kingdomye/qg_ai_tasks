"""
python树
Created by ricckker on 2024/9/11
Updated on 2024/9/12
"""
import queue


# 二叉树节点类
class BinaryNode:
    def __init__(self):
        self.name = None
        self.data = None
        
        self.leftChild = None
        self.rightChild = None

# 常规树节点类
class TreeNode:
    def __init__(self):
        self.name = None
        self.data = None

        self.childList = None

    def addChild(self, node):
        if self.childList == None:
            self.childList = [node]
        else:
            self.childList.append(node)

# 二叉树类
class BinaryTree:
    def __init__(self):
        self.root = None

    # 二叉树前序遍历
    def traversePreOrder(self, node):
        print(node.data, end = "->")

        if node.leftChild != None:
            self.traversePreOrder(node.leftChild)

        if node.rightChild != None:
            self.traversePreOrder(node.rightChild)

    # 二叉树中序遍历
    def traverseInOrder(self, node):
        if node.leftChild != None:
            self.traverseInOrder(node.leftChild)

        print(node.data, end = "->")

        if node.rightChild != None:
            self.traverseInOrder(node.rightChild)
    
    # 二叉树后序遍历
    def traversePostOrder(self, node):
        if node.leftChild != None:
            self.traversePreOrder(node.leftChild)

        if node.rightChild != None:
            self.traversePreOrder(node.rightChild)

        print(node.data, end = "->")
    
    # 二叉树层序遍历
    def traverseDepthFirst(self, node):
        myqueue = queue.Queue()
        myqueue.put(node)

        while myqueue.empty() != True:
            dequeueNode = myqueue.get()
            print(dequeueNode.data)
            if dequeueNode.leftChild != None:
                myqueue.put(dequeueNode.leftChild)

            if dequeueNode.rightChild != None:
                myqueue.put(dequeueNode.rightChild)

    # 有序二叉树：增加节点
    def addNode(self, val, node):
        newNode = BinaryNode()
        newNode.data = val

        if newNode.data < node.data:
            if node.leftChild == None:
                node.leftChild = newNode
            else:
                self.addNode(val, node.leftChild)
        else:
            if node.rightChild == None:
                node.rightChild = newNode
            else:
                self.addNode(val, node.rightChild)

    # 有序二叉树：查找节点(类比二分查找，时间复杂度为 logN)
    def searchNode(self, val, node):
        parent = self.root
        if node.data == val:
            return node, parent
        
        parent = node
        if val < node.data:
            if node.leftChild != None:
                return self.searchNode(val, node.leftChild)
        else:
            if node.rightChild != None:
                return self.searchNode(val, node.rightChild)

        return False, False

    # 有序二叉树：删除节点
    def deleteNode(self, val, node):
        deleteNode, deleteParentNode = self.searchNode(val, self.root)
        if deleteNode != False:
            # 情况一：待删除节点无子节点
            if deleteNode.leftChild == None and deleteNode.rightChild == None:
                if deleteNode == deleteParentNode.leftChild:
                    deleteParentNode.leftChild = None
                elif deleteNode == deleteParentNode.rightChild:
                    deleteParentNode.rightChild = None
            # 情况二：待删除节点有一个子节点
            elif (deleteNode.leftChild == None and deleteNode.rightChild != None) or (deleteNode.leftChild != None and deleteNode.rightChild == None):
                if deleteNode.leftChild != None:
                    pass

            # 情况三：待删除节点有两个子节点
    

class Tree:
    def __init__(self):
        self.root = None

    # 常规树前序遍历
    def traversePreOrder(self, node):
        print(node.name, end = "->")

        if node.childList != None:
            for childNode in node.childList:
                self.traversePreOrder(childNode)

    # 常规树后序遍历
    def traversePostOrder(self, node):
        if node.childList != None:
            for childNode in node.childList:
                self.traversePostOrder(childNode)
        
        print(node.name, end = "->")

    # 常规树层序遍历
    def traverseDepthFirst(self, node):
        myqueue = queue.Queue()
        myqueue.put(node)

        while myqueue.empty() != True:
            dequeueNode = myqueue.get()
            print(dequeueNode.name)

            if dequeueNode.childList != None:
                for childNode in dequeueNode.childList:
                    myqueue.put(childNode)


if __name__ == "__main__":
    mytree = BinaryTree()
    root = BinaryNode()
    root.data = 5

    mytree.root = root
    mytree.addNode(3, mytree.root)
    mytree.addNode(7, mytree.root)

    mynode, parentnode = mytree.searchNode(5, mytree.root)
    print(parentnode.data)
