// 边节点结构体
struct EdgeNode {
    bool mark; // 标记是否被搜索
    int vertex_i; // 边依附的顶点i
    EdgeNode* link_i; // 指向下一条依附于顶点i的边
    int vertex_j; // 边依附的顶点j
    EdgeNode* link_j; // 指向下一条依附于顶点j的边
    std::string info; // 存储边的信息

    EdgeNode(int i, int j, const std::string& info)
        : mark(false), vertex_i(i), link_i(nullptr), vertex_j(j), link_j(nullptr), info(info) {}
};

// 顶点节点结构体
struct VertexNode {
    std::string data; // 顶点存储的数据
    EdgeNode* first_edge; // 指向与该顶点相关的第一条边

    VertexNode(const std::string& data) : data(data), first_edge(nullptr) {}
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
            vertices[i] = VertexNode("Vertex " + std::to_string(i));
        }
    }

    // 添加边
    void addEdge(int i, int j, const std::string& info = "") {
        // 创建边节点
        EdgeNode* e = new EdgeNode(i, j, info);

        // 将边节点插入到顶点i的边链表中
        if (vertices[i].first_edge == nullptr) {
            vertices[i].first_edge = e;
        } else {
            EdgeNode* p = vertices[i].first_edge;
            while (p->link_i != nullptr) {
                p = p->link_i;
            }
            p->link_i = e;
        }

        // 将边节点插入到顶点j的边链表中
        if (vertices[j].first_edge == nullptr) {
            vertices[j].first_edge = e;
        } else {
            EdgeNode* p = vertices[j].first_edge;
            while (p->link_j != nullptr) {
                p = p->link_j;
            }
            p->link_j = e;
        }
    }
};
