#include <bits/stdc++.h>
using namespace std;

int T;
const int Maxb = 30;
int main () {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> T;
    while (T--) {
        int n;
        cin >> n;

        long long cnt[Maxb + 1] = {0};
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            for (int b = 0; b <= Maxb; b++) {
                if (x & (1 << b)) {
                    cnt[b]++;
                }
            }
        }
        long long ans = 0;
        for (int b = 0; b <= Maxb; b++) {
            long long c = cnt[b];
            ans += (1LL << b) * (c * (c - 1) / 2);
        }
        cout << ans << endl;
    }
    return 0;
}

