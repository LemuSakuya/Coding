#include <bits/stdc++.h>
using namespace std;

int n;
long long m, k;
vector<long long> a;

bool check(long long r) {
    long long cnt = 0;
    long long s = 0;
    for (int i = 0; i < n; i++) {
        s += a[i];
        if (s > m) {
            cnt++;
            s = 0;
            continue;
        }

        s += r * a[i];
        if (s > m) {
            cnt++;
            s = 0;
        }
    }
    return cnt <= k;
}

int main() {

    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    if (!(cin >> n >> m >> k)) return 0;
    
    a.resize(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
   
    long long l = 0, r = 1e12 + 10;
    long long ans = 0;
    
    while (l <= r) {
        long long mid = l + (r - l) / 2;
        if (check(mid)) {
            ans = mid;
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
    
    cout << ans << "\n";
    
    return 0;
}
