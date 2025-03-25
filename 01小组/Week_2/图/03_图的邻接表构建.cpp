// 定义图的邻接表结构
class Graph {
private:
    int V; // 图的顶点数
    std::vector<std::list<int>> adj; // 邻接表

public:
    // 构造函数
    Graph(int V) : V(V), adj(V) {}

    // 添加边
    void addEdge(int v, int w) {
        adj[v].push_back(w); // 添加无向边 v -> w
        adj[w].push_back(v); // 添加无向边 w -> v
    }

    // 打印邻接表
    void printGraph() {
        for (int v = 0; v < V; ++v) {
            std::cout << "Adjacency list：" << v << ": ";
            for (int neighbor : adj[v]) {
                std::cout << neighbor << " ";
            }
            std::cout << std::endl;
        }
    }
};