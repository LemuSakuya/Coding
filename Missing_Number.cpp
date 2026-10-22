#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long T;
    cin >> T;
    long long sum = (T + 1) * T / 2;

    for (int i = 0; i < T - 1; i++) {
        long long x;
        cin >> x;
        sum -= x;
    }

    cout << sum << endl;
    return 0;
}