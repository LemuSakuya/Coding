#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    string s;
    cin >> n >> s;

    int cnt = count(s.begin(), s.end(), '1');
    int l = s.find('1'), r = s.rfind('1');

    cout << (cnt < 3 ? cnt - 1 : r - l) << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();
}