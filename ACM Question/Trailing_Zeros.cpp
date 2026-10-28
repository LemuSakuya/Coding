#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll n;
    cin >> n;
    ll ans = 0;
    while(n) {
        n /= 5;
        ans += n;
    }

    cout << ans <<endl;
    return 0;
}