#include <bits/stdc++.h>

using namespace std;

int dx[] = {-1, 0, 1, 0}, dy[] = {0, 1, 0, -1};
int a[1000][1000];
int vis[1000][1000];
int n, m;
int xs, ys, xe, ye;
vector<pair<int, int> > ans;
vector<pair<int, int> > tmp;

void dfs(int x, int y) {
    if (x == xe && y == ye) {
        if (ans.empty()) {
            ans = tmp;
        }
        return;
    }
    for (int i = 0; i < 4; i++) {
        int u = x + dx[i], v = y + dy[i];
        if (u < 1 || v < 1 || u > n || v > m || vis[u][v] || a[u][v]) continue;
        vis[u][v] = 1;
        tmp.push_back(make_pair(u, v));
        dfs(u, v);
        vis[u][v] = 0;
        tmp.pop_back();
    }
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
            vis[i][j] = 0;
        }
    }
    cin >> xs >> ys >> xe >> ye;
    tmp.clear();
    ans.clear();
    tmp.push_back(make_pair(xs, ys));
    vis[xs][ys] = 1;
    dfs(xs, ys);
    
    if (ans.empty()) {
        cout << "No Path\n" << endl;
    } else {
        for (int i = ans.size() - 1; i >= 0; i--) {
            int x = ans[i].first;
            int y = ans[i].second;
            printf("(%d,%d)", x, y);
            if (i != 0) {
                printf("\t");
            }
            if ((ans.size() - i) % 5 == 0) {
                printf("\n");
            }
        }
        if (ans.size() % 5 != 0) {
            printf("\n");
        }
    }
}

int main() {
    int T = 1;
    while (T--) {
        solve();
    }
    return 0;
}