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

// struct point //相当于int 
// {
//     int x;
//     int y;
// };

// struct point createPoint(int x, int y)
// {
//     struct point temp;
//     temp.x = x;
//     temp.y = y;
//     return temp;
// }

// typedef double myType1;
// typedef char myType2;
// typedef string myType3;

// typedef struct
// {
//     int a;
//     char b;
//     string c;
// }Untitled;

// int main()
// {
//     // struct point p;
//     // p = createPoint(1,2);
//     // cout << p.x << "    " << p.y << endl;  
//     // struct point *pp;
//     // pp = &p;
//     // pp->x = 10;
//     // pp->y = 20;
//     // cout << pp->x << "    " << pp->y << endl;  
//     // (*pp).x = 20;
//     // (*pp).y = 10;
//     // cout << p.x << "    " << p.y << endl;  
   
//     // myType1 a = 10.0001;
//     // myType2 b = 'A';
//     // myType3 c = "fvhwidiwhfisw";
//     // cout << a << "  " << b << " " << c << endl;
//     // Untitled *p;
//     // p -> a = 1;
//     // p -> b = 'C';
//     // p -> c = "oaskjl";
//     // cout << (*p).a << " " << (*p).b << "    " << (*p).c << endl;
// }

// struct book
// {
//     int isbn;
//     char bookName[20];
//     double price;
// };

// int main()
// {
//     book b;
//     b.isbn = 764777;
//     strcpy(b.bookName, "java");
//     b.price = 90.1;

// }

#define MAXSIZE 100
typedef int ElemType;

typedef struct {
    // ElemType data[MAXSIZE];
    ElemType *data;
    int length;
}SeqList;

// void initList (SeqList *L) {
//     L -> length = 0;
    
// }//初始化顺序表

SeqList* initList () {
    SeqList *L = (SeqList*)malloc(sizeof(SeqList));

    if (!L) {
        return NULL;
    }// 检查内存分配

    L -> data = (ElemType*)malloc(sizeof(ElemType) * MAXSIZE);

    if (!L->data) {
        free(L);
        return NULL;
    }// 检查数据内存分配

    L -> length = 0;
    return L;

}//初始化顺序表

int appendElem (SeqList *L, ElemType e) {
    if (L -> length >= MAXSIZE) {
        cout << "The list is full" << endl;
        return 0;
    }

    L -> data[L -> length] = e;
    L -> length++;
    return 1;

}//在末尾添加元素

void listElem (SeqList *L) {
    for (int i = 0; i < L -> length; i++) {
        cout << L -> data[i] << "\t";
    }
    cout << endl;

}//检测元素是否存在

int insertElem (SeqList *L, int position, ElemType e) {

    if (position <= L -> length) {
        for (int i = L -> length; i >= position - 1; i--) {
            L -> data[i + 1] = L -> data[i];
        }
        L -> data[position - 1] = e;
        L -> length++; 
    }

    return 1;

}//插入元素

int deleteElem (SeqList *L, int position, ElemType *e) {
    *e = L -> data[position - 1];
    if (position < L -> length) {
        for (int i = position; i < L -> length; i++) {
            L -> data[i - 1] = L -> data[i];
        }
    }
    L -> length--;
    return 1;

}//删除元素

int findElem (SeqList *L, ElemType e) {
    for (int i = 0; i < L -> length; i++) {
        if (L -> data[i] == e) {
            return i + 1;
        }
    }
    return 0;

}//查找元素

int main() {
    SeqList *list = initList();
    cout << "Perfect Initialise" << endl;
    cout << "It cost " << list -> length << endl;
    cout << "It memory is "  << sizeof(list -> data) << endl;

    for (int i = 10; i <= 14; i++) {
        appendElem(list, i);
    }

    cout << "Now the list is " << endl;
    listElem(list);
    cout << "Now it cost " << list -> length << endl;

    insertElem(list, 2, 4);
    cout << "Now the list is " << endl;
    listElem(list);
    cout << "Now it cost " << list -> length << endl;

    ElemType deletedata;
    deleteElem(list, 4, &deletedata);
    cout << "The delete data is " << deletedata << endl;
    cout << "Now the list is " << endl;
    listElem(list);
    cout << "Now it cost " << list -> length << endl;

    ElemType finddata = 14;
    cout << "your find data's position is " << findElem(list, finddata) << endl;
    cout << "Now the list is " << endl;
    listElem(list);
    cout << "Now it cost " << list -> length << endl;

    free(list);
}