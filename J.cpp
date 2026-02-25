#include <bits/stdc++.h>
using namespace std;

int T;
int main () {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> T;
    long double sum = 0;
    while (T--) {
        long double sx, sy, tx, ty;
        cin >> sx >> sy >> tx >> ty;

        long double dx = sx - tx;
        long double dy = sy - ty;
        sum += sqrt(dx * dx + dy * dy);
    }

    long double x, y;
    cin >> x >> y;

    long double ans = sum * 2;
    cout.setf(ios::fixed);
    cout << setprecision(10) << (double)ans << endl;

    return 0;
}

