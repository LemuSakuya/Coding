#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;

    if (n == 1) {
        cout << 0 << '\n';
        return;
    }

    int k = (n + 1) / 2;
    cout << k << '\n';

    for (int i = 1; i <= k; ++i)
        cout << i << ' ' << i + n / 2 - 1 << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();

    return 0;
}