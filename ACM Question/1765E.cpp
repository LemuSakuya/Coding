#include<bits/stdc++.h>
using namespace std;

int T;
int main() {
	ios::sync_with_stdio(false);

	cin >> T;
	while (T--) {
		int n, a, b;
        cin >> n >> a >> b;
		if (a > b) {
            cout << "1\n";
        } else {
            cout << (int)ceil(1.0 * n / a) << endl;
        }
	}
	return 0;
}