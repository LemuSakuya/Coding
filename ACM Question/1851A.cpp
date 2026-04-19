#include <bits/stdc++.h>
using namespace std;

int T;
const int maxh = 55;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> T;
    while (T--) {
        int n, m, k, H;
        cin >> n >> m >> k >> H;
        long long h[maxh];
        for (int i = 0; i < n; i++) {
            cin >> h[i];
        }
        int ans = 0;
        long long maxdif = 1LL * k * (m - 1);
        for (int i = 0; i < n; i++) {
            long long dif = llabs(h[i] - H);
            if (dif == 0) {
                continue;
            }
            if (dif % k == 0 && dif <= maxdif) {
                ans++;
            }
        }
        cout << ans << endl;
    }
}