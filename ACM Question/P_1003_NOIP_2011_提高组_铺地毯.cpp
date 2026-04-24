#include <bits/stdc++.h>
#define int long long
using namespace std;

const int MAXN = 1e5 + 5;

int a[MAXN], b[MAXN], g[MAXN], k[MAXN];
int n, ans = -1;
signed main () {
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> a[i] >> b[i] >> g[i] >> k[i];
    }

    int x, y;
    cin >> x >> y;
    for (int i = 0; i < n; i++) {
        if ((x >= a[i] && x <= a[i] + g[i]) && (y >= b[i] && y <= b[i] + k[i])) {
            ans = i + 1;
        }
    }

    cout << ans << endl;
    return 0;
}