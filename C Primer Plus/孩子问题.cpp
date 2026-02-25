#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<int, int> pii;

const int MAXN = 205;
const int MOD = 1e9 + 7;
const int INF = 0x3f3f3f3f;

#define rep(i, a, b) for(int i = (a); i <= (b); i++)
#define per(i, a, b) for(int i = (a); i >= (b); i--)
#define pb push_back
#define mp make_pair
#define all(x) (x).begin(), (x).end()
#define fi first
#define se second
#define sz(x) ((int)(x).size())

int path[MAXN], cnt;
ll ans = 0;

void dfs(int current_val, int rem) {
    if (rem == 0) {
        ans++;
        cout << "Sol " << ans << ": ";
        rep(i, 0, cnt - 1) {
            cout << (50 - path[i]) << (i == cnt - 1 ? "" : " ");
        }
        cout << "\n";
        return;
    }

    if (current_val == 0) return;
    if (rem > current_val * (current_val + 1) / 2) return;

    per(k, 1, 0) { 
        if (rem >= k * current_val) {
            rep(_, 1, k) path[cnt++] = current_val;
            
            dfs(current_val - 1, rem - k * current_val);
            
            rep(_, 1, k) cnt--;
        }
    }
}

void solve() {
    cout << "Start searching (each number at most ONCE)..." << endl;
    dfs(25, 49);
    cout << "Total unique solutions found: " << ans << endl;
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);
    
    int T = 1;
    while(T--) {
        solve();
    }
    
    return 0;
}