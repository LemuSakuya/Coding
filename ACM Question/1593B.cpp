#include <bits/stdc++.h>
using namespace std;

int T;
int main() {
    cin >> T;
    while (T--) {
        string str;
        cin >> str;
        int ans1 = 0, ans2 = 0;
        int n = str.length();
        for (int i = n - 1; i >= 0; i--) {
            if (str[i] != '0') {
                ans1++;
            } else {
                for (int j = i - 1; j >= 0; j--) {
                    if (str[j] == '0' || str[j] == '5') {
                        break;
                    } else {
                        ans1++;
                    }
                }
                break;
            }
        }
        for (int i = n - 1; i >= 0; i--) {
            if (str[i] != '5') {
                ans2++;
            } else {
                for (int j = i - 1; j >= 0; j--) {
                    if (str[j] == '2' || str[j] == '7') {
                        break;
                    } else {
                        ans2++;
                    }
                }
                break;
            }
        }
        cout << min(ans1, ans2) << endl;
    }
}