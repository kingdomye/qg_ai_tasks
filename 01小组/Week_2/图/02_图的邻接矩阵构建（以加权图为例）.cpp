#include <iostream>
#include <vector>
#include <climits>

using namespace std;

// 构建加权图的邻接矩阵
void buildWeightedGraph(int vertices, int edges, vector<vector<int>>& adjMatrix) {
    for (int i = 0; i < vertices; ++i) {
        for (int j = 0; j < vertices; ++j) {
            adjMatrix[i][j] = (i == j) ? 0 : INT_MAX;
        }
    }

    cout << "请输入每条边的起点、终点和权重（用空格分隔）：" << endl;
    for (int i = 0; i < edges; ++i) {
        int start, end, weight;
        cin >> start >> end >> weight;

        if (start < 0 || start >= vertices || end < 0 || end >= vertices) {
            cout << "输入的顶点编号无效，请重新输入！" << endl;
            --i; // 重新输入这条边
            continue;
        }
        adjMatrix[start][end] = weight;
    }
}

// 打印邻接矩阵
void printAdjMatrix(const vector<vector<int>>& adjMatrix) {
    int vertices = adjMatrix.size();
    cout << "加权图的邻接矩阵为：" << endl;
    for (int i = 0; i < vertices; ++i) {
        for (int j = 0; j < vertices; ++j) {
            if (adjMatrix[i][j] == INT_MAX) {
                cout << "INF ";
            } else {
                cout << adjMatrix[i][j] << " ";
            }
        }
        cout << endl;
    }
}

int main() {
    int vertices, edges;
    cout << "请输入顶点数："; cin >> vertices;
    cout << "请输入边数："; cin >> edges;

    vector<vector<int>> adjMatrix(vertices, vector<int>(vertices));			// 创建邻接矩阵
    buildWeightedGraph(vertices, edges, adjMatrix);			// 构建加权图的邻接矩阵
    printAdjMatrix(adjMatrix);			// 打印邻接矩阵

    return 0;
}