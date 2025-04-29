#include <bits/stdc++.h>

void hanoi(int n, char src, char aux, char dst, int *sum, int show_steps) {
    if (n == 1) {
        (*sum)++;
        if (show_steps) {
            printf("%c-->%c\n", src, dst);
        }
        return;
    }
    
    hanoi(n - 1, src, dst, aux, sum, show_steps);
    (*sum)++;
    if (show_steps) {
        printf("%c-->%c\n", src, dst);
    }
    hanoi(n - 1, aux, src, dst, sum, show_steps);
}

int main() {
    int n;
    scanf("%d", &n);
    
    if (n <= 0) {
        printf("ERROR");
        return 0;
    }
    
    int sum = 0;
    int show_steps = (n < 6);
    
    hanoi(n, 'A', 'B', 'C', &sum, show_steps);
    printf("moves=%d", sum);
    
    return 0;
}