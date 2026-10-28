#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    if (n == 1) {
        cout << n << endl;
        return 0;
    }

    if (n <= 3) {
        cout << "NO SOLUTION" << endl;
        return 0;
    }

    for (int i = 2; i <= n; i+=2) {
        cout << i << ' ';
    }

    for (int j = 1; j <= n; j+=2) {
        cout << j << ' ';
    }

    cout << endl;
    return 0;
}


