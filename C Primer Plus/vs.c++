#include <bits/stdc++.h>

using namespace std;

// void swap(int *a, int *b)
// {
//     int temp = *a;
//     *a = *b;
//     *b = temp;
//     cout << a << "  " << b << endl;
// }


// int main()
// {
//     int n = 10;
//     int m = 5;
//     cout << n << "  " << m << endl;
//     swap(&n,&m);
//     cout << n << "  " << m << endl;

//     return 0;
    
// }

// int main()
// {
//     int a[] = {0,1,2,3,4,5};
//     int *p = a;
//     cout << *p << " " << a << "  " << p << endl;
// }

struct point
{
    int x;
    int y;
};

struct point createPoint(int x, int y)
{
    struct point temp;
    temp.x = x;
    temp.y = y;
    return temp;
}

typedef double myType1;
typedef char myType2;
typedef string myType3;

typedef struct
{
    int a;
    char b;
    string c;
}Untitled;

int main()
{
    // struct point p;
    // p = createPoint(1,2);
    // cout << p.x << "    " << p.y << endl;  
    // struct point *pp;
    // pp = &p;
    // pp->x = 10;
    // pp->y = 20;
    // cout << pp->x << "    " << pp->y << endl;  
    // (*pp).x = 20;
    // (*pp).y = 10;
    // cout << p.x << "    " << p.y << endl;  
   
    myType1 a = 10.0001;
    myType2 b = 'A';
    myType3 c = "fvhwidiwhfisw";
    cout << a << "  " << b << " " << c << endl;
    Untitled *p;
    p -> a = 1;
    p -> b = 'C';
    p -> c = "oaskjl";
    cout << (*p).a << " " << (*p).b << "    " << (*p).c << endl;
} 