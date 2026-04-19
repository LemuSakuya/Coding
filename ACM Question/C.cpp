#include <bits/stdc++.h>
using namespace std;

int main () {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    if (!(cin >> n >> m)) return 0;
    int total = n * m;

    long long cntR[256] = {0};
    long long cntG[256] = {0};
    long long cntB[256] = {0};

    for (int i = 0; i < total; i++) {
        string s;
        cin >> s;
        int r = stoi(s.substr(0, 3));
        int g = stoi(s.substr(4, 3));
        int b = stoi(s.substr(8, 3));
        cntR[r]++;
        cntG[g]++;
        cntB[b]++;
    }

    auto solve = [](long long cnt[]) -> long long {
        long long best = -1;
        for (int c = 0; c <= 255; c++) {
            long long cur = 0;
            for (int v = 0; v <= 255; v++) {
                long long d = c - v;
                cur += cnt[v] * d * d;
            }
            if (best == -1 || cur < best) best = cur;
        }
        return best;
    };

    long long ans = 0;
    ans += solve(cntR);
    ans += solve(cntG);
    ans += solve(cntB);
    cout << ans << endl;
    return 0;
}

