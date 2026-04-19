#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k;
    if (!(cin >> k)) {
        return 0;
    }

    const int H = 5;
    const int W = 36;
    const char base[H][W + 1] = {
        "*****...******...***...**...**....**",
        "**......**.......****..**...**....**",
        "*****...**.......**.**.**...**....**",
        "...**...**.......**..****...**....**",
        "*****...******...**...***...********"
    };

    char orig[H][W];
    for (int i = 0; i < H; i++) {
        for (int j = 0; j < W; j++) {
            orig[i][j] = base[i][j];
        }
    }

    int H2 = H * k, W2 = W * k;
    char ans[H * 5][W * 5];
    for (int i = 0; i < H2; i++) {
        for (int j = 0; j < W2; j++) {
            ans[i][j] = orig[i / k][j / k];
        }
    }

    for (int i = 0; i < H2; i++) {
        for (int j = 0; j < W2; j++) {
            cout << ans[i][j];
        }
        cout << endl;
    }
    return 0;
}