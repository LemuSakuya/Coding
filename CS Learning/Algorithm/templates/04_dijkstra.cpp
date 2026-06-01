using ll = long long;
const ll LINF = (1LL << 62);

vector<ll> dijkstra(int s, const vector<vector<pair<int,int>>>& g) {
    int n = (int)g.size() - 1;
    vector<ll> dist(n + 1, LINF);
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<>> pq;
    dist[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
