#include <bits/stdc++.h>
using namespace std;

int main() {
    long long x, y;
    if (!(cin >> x >> y)) return 0;

    vector<long long> dp(y + 20, 1e18);
    dp[0] = 0;

    for (int i = 0; i < y + 6; i++) {
        dp[i + 1] = min(dp[i + 1], dp[i] + x * 10);

        dp[i + 2] = min(dp[i + 2], dp[i] + 99 + x * 10);

        dp[i + 6] = min(dp[i + 6], dp[i] + 50 * x);
    }

    long long ans = 1e18;
    for (int i = y; i <= y + 6; i++) {
        ans = min(ans, dp[i]);
    }

    if (ans % 10 == 0) {
        cout << ans / 10 << "\n";
    } else {
        cout << ans / 10 << "." << ans % 10 << "\n";
    }
    
    return 0;
}