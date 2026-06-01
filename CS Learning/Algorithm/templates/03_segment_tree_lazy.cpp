struct SegTree {
    struct Node { long long sum = 0, lazy = 0; };
    int n;
    vector<Node> tr;
    SegTree(int n = 0) { init(n); }
    void init(int n_) { n = n_; tr.assign(4 * n + 5, {}); }
    void apply(int p, int l, int r, long long v) {
        tr[p].sum += v * (r - l + 1);
        tr[p].lazy += v;
    }
    void push(int p, int l, int r) {
        if (!tr[p].lazy || l == r) return;
        int m = (l + r) >> 1;
        apply(p << 1, l, m, tr[p].lazy);
        apply(p << 1 | 1, m + 1, r, tr[p].lazy);
        tr[p].lazy = 0;
    }
    void rangeAdd(int p, int l, int r, int ql, int qr, long long v) {
        if (ql <= l && r <= qr) return apply(p, l, r, v);
        push(p, l, r);
        int m = (l + r) >> 1;
        if (ql <= m) rangeAdd(p << 1, l, m, ql, qr, v);
        if (qr > m) rangeAdd(p << 1 | 1, m + 1, r, ql, qr, v);
        tr[p].sum = tr[p << 1].sum + tr[p << 1 | 1].sum;
    }
    long long query(int p, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return tr[p].sum;
        push(p, l, r);
        int m = (l + r) >> 1;
        long long ans = 0;
        if (ql <= m) ans += query(p << 1, l, m, ql, qr);
        if (qr > m) ans += query(p << 1 | 1, m + 1, r, ql, qr);
        return ans;
    }
};
