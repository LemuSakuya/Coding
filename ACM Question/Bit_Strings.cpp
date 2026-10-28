#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll MOD = 1e9 + 7;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll n;
    cin >> n;
    ll sum = 1;
    while (n--) {
        sum = (sum * 2) % MOD;
    }

    cout << sum << endl;
    return 0;
}