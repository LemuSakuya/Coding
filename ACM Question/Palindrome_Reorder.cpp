#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int cnt[26] = {0};
    string s;
    cin >> s;
    for (char c : s) {
        cnt[c - 'A']++;
    }

    int odd = 0;
    string mid = "";
    for (int i = 0; i < 26; i++) {
        if (cnt[i] % 2 == 1) {
            odd++;
            mid = (char)('A' + i);
        }
    }

    if (odd > 1) {
        cout << "NO SOLUTION" << endl;
        return 0;
    } else {
        string half = "";
        for (int i = 0; i < 26; i++) {
            half += string(cnt[i] / 2, (char)('A' + i));
        }
        cout << half << mid << string(half.rbegin(), half.rend()) << endl;
        return 0;
    }
}