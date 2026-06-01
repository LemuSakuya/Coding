long long qpow(long long a, long long b, long long mod) {
    long long r = 1 % mod;
    while (b) {
        if (b & 1) r = (__int128)r * a % mod;
        a = (__int128)a * a % mod;
        b >>= 1;
    }
    return r;
}

struct Comb {
    long long mod;
    vector<long long> fac, ifac;
    Comb(int n, long long mod): mod(mod), fac(n + 1), ifac(n + 1) {
        fac[0] = 1;
        for (int i = 1; i <= n; ++i) fac[i] = fac[i - 1] * i % mod;
        ifac[n] = qpow(fac[n], mod - 2, mod);
        for (int i = n; i >= 1; --i) ifac[i - 1] = ifac[i] * i % mod;
    }
    long long C(int n, int k) const {
        if (k < 0 || k > n) return 0;
        return fac[n] * ifac[k] % mod * ifac[n - k] % mod;
    }
};
