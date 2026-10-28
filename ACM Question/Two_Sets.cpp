#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ll n;
    cin >> n;
    ll sum = (n + 1) * n / 2;
    if (sum % 2 != 0) {
        cout << "NO" << endl;
        return 0;
    } else {
        cout << "YES" << endl;

        vector<ll> a, b;
        ll tag = sum / 2;
        for (ll i = n; i >= 1; i--) {
            if (i <= tag) { 
                a.push_back(i);
                tag -= i;
            } else {
                b.push_back(i);
            }
        }

        cout << a.size() << endl;
        for (auto i : a) {
            cout << i << " ";
        }
        cout << endl;

        cout << b.size() << endl;
        for (auto i : b) {
            cout << i << " ";
        }
        cout << endl;

        return 0;
    }
}