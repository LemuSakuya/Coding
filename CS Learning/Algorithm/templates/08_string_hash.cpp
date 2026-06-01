struct StringHash {
    static const long long mod1 = 1000000007;
    static const long long mod2 = 1000000009;
    static const long long base = 911382323;
    vector<long long> h1, h2, p1, p2;
    StringHash(const string& s) {
        int n = s.size();
        h1.assign(n + 1, 0); h2.assign(n + 1, 0);
        p1.assign(n + 1, 1); p2.assign(n + 1, 1);
        for (int i = 0; i < n; ++i) {
            p1[i + 1] = p1[i] * base % mod1;
            p2[i + 1] = p2[i] * base % mod2;
            h1[i + 1] = (h1[i] * base + s[i]) % mod1;
            h2[i + 1] = (h2[i] * base + s[i]) % mod2;
        }
    }
    pair<long long,long long> get(int l, int r) const { // [l, r)
        long long x = (h1[r] - h1[l] * p1[r - l]) % mod1;
        long long y = (h2[r] - h2[l] * p2[r - l]) % mod2;
        if (x < 0) x += mod1;
        if (y < 0) y += mod2;
        return {x, y};
    }
};
