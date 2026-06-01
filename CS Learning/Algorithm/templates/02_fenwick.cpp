template<class T>
struct Fenwick {
    int n;
    vector<T> t;
    Fenwick(int n = 0) { init(n); }
    void init(int n_) { n = n_; t.assign(n + 1, T{}); }
    void add(int i, T v) {
        for (; i <= n; i += i & -i) t[i] += v;
    }
    T sumPrefix(int i) const {
        T r{};
        for (; i > 0; i -= i & -i) r += t[i];
        return r;
    }
    T sumRange(int l, int r) const {
        return sumPrefix(r) - sumPrefix(l - 1);
    }
};
