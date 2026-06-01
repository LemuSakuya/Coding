struct Dinic {
    struct Edge { int to, rev; long long cap; };
    int n;
    vector<vector<Edge>> g;
    vector<int> level, it;
    Dinic(int n = 0) { init(n); }
    void init(int n_) { n = n_; g.assign(n + 1, {}); level.resize(n + 1); it.resize(n + 1); }
    void addEdge(int u, int v, long long c) {
        Edge a{v, (int)g[v].size(), c};
        Edge b{u, (int)g[u].size(), 0};
        g[u].push_back(a); g[v].push_back(b);
    }
    bool bfs(int s, int t) {
        fill(level.begin(), level.end(), -1);
        queue<int> q;
        level[s] = 0; q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto &e : g[u]) if (e.cap > 0 && level[e.to] == -1) {
                level[e.to] = level[u] + 1;
                q.push(e.to);
            }
        }
        return level[t] != -1;
    }
    long long dfs(int u, int t, long long f) {
        if (u == t) return f;
        for (int &i = it[u]; i < (int)g[u].size(); ++i) {
            Edge &e = g[u][i];
            if (e.cap > 0 && level[e.to] == level[u] + 1) {
                long long ret = dfs(e.to, t, min(f, e.cap));
                if (ret) {
                    e.cap -= ret;
                    g[e.to][e.rev].cap += ret;
                    return ret;
                }
            }
        }
        return 0;
    }
    long long maxflow(int s, int t) {
        long long flow = 0, pushed;
        while (bfs(s, t)) {
            fill(it.begin(), it.end(), 0);
            while ((pushed = dfs(s, t, (1LL << 62)))) flow += pushed;
        }
        return flow;
    }
};
