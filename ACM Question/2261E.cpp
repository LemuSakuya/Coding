#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, k;
    string s;
    cin >> n >> k >> s;

    vector<int> st;
    st.reserve(n / 2);

    int c = 0, ans = 0;

    for (char ch : s) {
        if (ch == '(') {
            st.push_back(c);

            int j = lower_bound(st.begin(), st.end(), c - k)
                    - st.begin();

            int depth = st.size();
            ans = max(ans, depth - j);

            if (c <= k)
                ans = max(ans, depth + k);
        } else {
            st.pop_back();
            ++c;
        }
    }

    cout << min(ans, n / 2) << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();

    return 0;
}