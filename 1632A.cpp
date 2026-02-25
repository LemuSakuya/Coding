#include <bits/stdc++.h>
using namespace std;

int long long T, n;
char str[100005];

int main() {
    cin >> T;
    while (T--){
        cin >> n >> str;
        if (n == 1 || (n == 2 && str[0]!=str[1]))
        cout << "YES\n";
        else
        cout << "NO\n";
    }
    return 0;
}