#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    cin >> T;
    while (T--) {
        string s1, s2;
        cin >> s1 >> s2;
        int j = 0;
        for (int k = 1; k < (int)s2.size(); k++)
            if (s2[k] < s2[j]) j = k;
        for (int i = 0; i < (int)s1.size(); i++) {
            if (s1[i] > s2[j]) {
                swap(s1[i], s2[j]);
                break;
            }
        }
        cout << s1 << '\n' << s2 << '\n';
    }
    return 0;
}
