#include <bits/stdc++.h>
using namespace std;

int main() {
    int N, k;
    char c;
    string S;
    
    cin >> N >> c >> k;
    cin >> S;
    
    vector<int> pos;
    for (int i = 0; i < N; i++) {
        if (S[i] == c) {
            pos.push_back(i);
        }
    }
    
    int min_len = 1e9;
    int start_idx = -1;
    
    for (int i = 0; i <= (int)pos.size() - k; i++) {

        int current_len = pos[i + k - 1] - pos[i] + 1;
        
        if (current_len < min_len) {
            min_len = current_len;
            start_idx = pos[i];
        }
    }
    
    cout << S.substr(start_idx, min_len) << endl;
    
    return 0;
}