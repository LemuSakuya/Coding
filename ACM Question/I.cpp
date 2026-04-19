#include <bits/stdc++.h>
using namespace std;

const int T = 6;
int main () {
    int t = T;
    while (t--) {
        long long n;
        cin >> n;
        long long ans = n * (n - 1) / 2;
        cout << ans;
        if (t) {
            cout << ' ';
        }
    }
    cout << endl;
    return 0;
}