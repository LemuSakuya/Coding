#include <iostream>
using namespace std;

//1、比较基础的分治算法
int n;
int a[100000];
int x;


int d(int left, int right){
    if(left >= right){
        return -1;
    }
    int mid = (left + right) / 2;
    if(a[mid] == x){
        return mid;
    }
    else if(a[mid] > x){
        return d(left, mid);
    }
    else{
        return d(mid + 1, right);
}
}

int main(){
    cin >> n;
    int left = 0, right = n - 1;
    for (int i = 0; i < n; i++){
        cin>>a[i];
    } 
    cin>>x;
    cout << d(left, right) + 1 << endl;
    return 0;
}

