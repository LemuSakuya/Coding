#include <bits/stdc++.h>
using namespace std;

int T;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        if (n % 7 == 0) {
            cout << n << "\n";
            continue;
        }
        int a = n / 10;
        for (int d = 0; d <= 9; d++) {
            int x = a * 10 + d;
            if (x % 7 == 0) {
                cout << x << "\n";
                break;
            }
        }
    }
    return 0;
}