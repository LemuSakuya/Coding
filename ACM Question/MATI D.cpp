#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int n;
    long long k1, k2;
    if (!(cin >> n >> k1 >> k2)) return 0;
    
    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    
    long long min_cost = -1;

    for (int S = 0; S <= 31; S++) {

        long long current_cost = S * k1;
        
        for (int i = 0; i < n; i++) {
            long long x = a[i] >> S;

            while (x > k2) {

                x -= (x & (-x));
                current_cost++;
            }
        }

        if (min_cost == -1 || current_cost < min_cost) {
            min_cost = current_cost;
        }
    }
    
    // 输出
    cout << min_cost << "\n";
    
    return 0;
}
