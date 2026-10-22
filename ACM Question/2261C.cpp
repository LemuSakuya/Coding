#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    int odd = 0;
    for (int i = 0, x; i < n; ++i) {
        cin >> x;
        odd += x & 1;
    }

    bool lose = (n == 2 && odd == 1) ||
                (n == 3 && odd == 3);

    cout << (lose ? "Larpity" : "Moggity") << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();

    return 0;
}