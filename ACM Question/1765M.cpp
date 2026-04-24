#include <bits/stdc++.h>
using namespace std;

int T;
int main() {
	cin>>T;
	while(T--) {
		int n;
		cin >> n;
		int top = 1;
		for(int i = 2; i <= sqrt(n); i++)
			if (n % i == 0) {
				top = i;
				break;
			}
		if (top != 1) {
		    top = n / top;
        }
		if(n % 2 == 0) {
			cout << n/2 << ' ' <<  n / 2 << endl;
        } else {
			cout << top << ' ' << n - top << endl;
        }
	}
    return 0;
}
