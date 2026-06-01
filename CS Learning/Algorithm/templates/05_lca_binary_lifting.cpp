const int LOG = 20;
vector<vector<int>> g;
vector<array<int, LOG>> up;
vector<int> dep;

void dfs_lca(int u, int p) {
    up[u][0] = p;
    for (int k = 1; k < LOG; ++k) up[u][k] = up[up[u][k - 1]][k - 1];
    for (int v : g[u]) if (v != p) {
        dep[v] = dep[u] + 1;
        dfs_lca(v, u);
    }
}

int lca(int a, int b) {
    if (dep[a] < dep[b]) swap(a, b);
    int diff = dep[a] - dep[b];
    for (int k = 0; k < LOG; ++k) if (diff >> k & 1) a = up[a][k];
    if (a == b) return a;
    for (int k = LOG - 1; k >= 0; --k) {
        if (up[a][k] != up[b][k]) a = up[a][k], b = up[b][k];
    }
    return up[a][0];
}
