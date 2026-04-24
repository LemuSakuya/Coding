#include <bits/stdc++.h>
using namespace std;

int T;
const int maxn = 200000 + 5;
int c[maxn];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> T;
    while (T--) {
        int n, k;
        cin >> n >> k;
        for (int i = 0; i < n; i++) {
            cin >> c[i];
        }

        int fst = c[0];
        int lst = c[n - 1];

        if (fst == lst) {
            int cnt = 0;
            for (int i = 0; i < n; i++) {
                if (c[i] == fst) {
                    cnt++;
                }
            }
            cout << (cnt >= k ? "YES" : "NO") << endl;
            continue;
        }

        int pos1 = -1, pos2 = -1;
        int cnt = 0;
        for (int i = 0; i < n; i++) {
            if (c[i] == fst) {
                cnt++;
                if (cnt == k) {
                    pos1 = i;
                    break;
                }
            }
        }
        cnt = 0;
        for (int i = n - 1; i >= 0; i--) {
            if (c[i] == lst) {
                cnt++;
                if (cnt == k) {
                    pos2 = i;
                    break;
                }
            }
        }

        if (pos1 != -1 && pos2 != -1 && pos1 < pos2) {
            cout << "YES" << endl;
        } else {
            cout << "NO" << endl;
        }
    }
    return 0;
}

