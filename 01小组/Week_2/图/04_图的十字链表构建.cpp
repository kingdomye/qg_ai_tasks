// 弧节点结构体
struct EdgeNode {
    int tailvex; // 弧尾顶点编号
    int headvex; // 弧头顶点编号
    EdgeNode* hlink; // 指向弧头相同的下一条弧
    EdgeNode* tlink; // 指向弧尾相同的下一条弧
    std::string info; // 弧存储的信息
};

// 顶点节点结构体
struct VertexNode {
    std::string data; // 顶点存储的数据
    int indegree; // 顶点的入度
    int outdegree; // 顶点的出度
    EdgeNode* firstin; // 指向以该顶点为弧头的第一条弧
    EdgeNode* firstout; // 指向以该顶点为弧尾的第一条弧
};

// 图类
class Graph {
private:
    int V; // 图的顶点数
    std::vector<VertexNode> vertices; // 顶点数组

public:
    // 构造函数
    Graph(int V) : V(V), vertices(V) {
        for (int i = 0; i < V; ++i) {
            vertices[i].data = "Vertex " + std::to_string(i);
            vertices[i].indegree = 0;
            vertices[i].outdegree = 0;
            vertices[i].firstin = nullptr;
            vertices[i].firstout = nullptr;
        }
    }

    // 添加弧
    void addEdge(int tail, int head, const std::string& info = "") {
        // 创建新的弧节点
        EdgeNode* e = new EdgeNode{tail, head, nullptr, nullptr, info};

        // 更新弧尾顶点的出度和链表
        vertices[tail].outdegree++;
        if (vertices[tail].firstout == nullptr) {
            vertices[tail].firstout = e;
        } else {
            EdgeNode* p = vertices[tail].firstout;
            while (p->tlink != nullptr) {
                p = p->tlink;
            }
            p->tlink = e;
        }

        // 更新弧头顶点的入度和链表
        vertices[head].indegree++;
        if (vertices[head].firstin == nullptr) {
            vertices[head].firstin = e;
        } else {
            EdgeNode* p = vertices[head].firstin;
            while (p->hlink != nullptr) {
                p = p->hlink;
            }
            p->hlink = e;
        }
    }
};