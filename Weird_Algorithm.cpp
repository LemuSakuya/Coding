#include <bits/stdc++.h>
using namespace std;

int main() {
    long long T;
    cin >> T;
    cout << T;
    while (T != 1) {
        if (T % 2 == 0) {
            T /= 2;
        } else {
            T = T * 3 + 1;
        }
        cout << " " << T;
    }

    cout << endl;
    return 0;
}