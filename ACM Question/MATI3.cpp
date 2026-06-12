#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<ll> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());

    vector<ll> diff;
    for (int i = 1; i < n; i++) {
        diff.push_back(a[i] - a[i - 1]);
    }
    sort(diff.begin(), diff.end());

    vector<ll> prefix(diff.size() + 1, 0);
    for (int i = 0; i < (int)diff.size(); i++) {
        prefix[i + 1] = prefix[i] + diff[i];
    }

    int q;
    cin >> q;

    ll lastans = 0;
    while (q--) {
        ll x;
        cin >> x;

        ll y = x ^ lastans;
        int cnt = upper_bound(diff.begin(), diff.end(), y) - diff.begin();
        lastans = y + prefix[cnt] + (ll)(diff.size() - cnt) * y;

        cout << lastans << '\n';
    }

    return 0;
}
