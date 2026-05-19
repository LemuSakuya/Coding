#include<bits/stdc++.h> 

int main() {
    int a[3];
    scanf("%d %d %d", &a[0], &a[1], &a[2]);
    int odd = (a[0] & 1) + (a[1] & 1) + (a[2] & 1);
    if (odd == 0) puts("even");
    else if (odd == 3) puts("odd");
    else {
        int target = (odd == 1) ? 1 : 0;  // 1奇时找奇，2奇时找偶
        for (int i = 0; i < 3; i++)
            if ((a[i] & 1) == target) { printf("%d\n", a[i]); break; }
    }
    return 0;
}
