#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    int l = INT_MAX, r = 0;
    for (int i = 0, x; i < n; ++i) {
        cin >> x;
        l = min(l, x);
        r = max(r, x);
    }

    while (l < r) l |= l + 1;

    cout << l << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();

    return 0;
}