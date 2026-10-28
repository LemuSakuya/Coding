#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ll T;
    cin >> T;

    while (T--) {
        ll a, b;
        cin >> a >> b;

        if (a <= b * 2 && b <= a * 2 && (a + b) % 3 == 0) {
            cout << "YES" << endl;
        } else { 
            cout << "NO" << endl;
        }
    }

    return 0;
}