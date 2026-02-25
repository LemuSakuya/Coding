#include <bits/stdc++.h>
using namespace std;

int T;
int main () {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> T;
    while (T--) {
        long long n;
        cin >> n;
        long long mod = n % 7;
        if (mod == 0 || mod == 2) {
            cout << "ice" << endl;
        } else {
            cout << "Orange" << endl;
        }
    }
    return 0;
}