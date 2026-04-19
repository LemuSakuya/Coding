#include <bits/stdc++.h>
using namespace std;

int T;
const int maxn = 200000 + 5;
int a[maxn], b[maxn];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        for (int i = 0; i < n; i++) {
            cin >> a[i];
            b[i] = a[i];
        }
        sort(b, b + n);

        bool ok = true;
        for (int i = 0; i < n; i++) {
            if ((a[i] & 1) != (b[i] & 1)) {
                ok = false;
                break;
            }
        }
        cout << (ok ? "YES" : "NO") << endl;
    }
    return 0;
}

