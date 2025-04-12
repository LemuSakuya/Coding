#include <bits/stdc++.h>
using namespace std;

typedef int ElemType;

typedef struct node {
    ElemType data;
    struct node *next;
} Node;

Node* initList() {
    Node *head = (Node*)malloc(sizeof(Node));
    head -> data = 0;
    head -> next = NULL;
    return head;
}//头节点（初始化）

int insertHead (Node* L, ElemType e) {
    Node *p = (Node*)malloc(sizeof(Node));
    p -> data = e;
    p -> next = L -> next;
    L -> next = p;
    return 1;
}//头插入

void listNode (Node *L) {
    Node *p = L -> next;
    while (p != NULL) {
        printf("%d\n", p -> data);
        p = p -> next;

    }
    printf("\n");
}//列出链表

Node* get_tail(Node *L) {
    Node *p = L;
    while(p -> next != NULL) {
        p = p -> next;
    }
    return p;
}//获取尾节点

Node* insertTail (Node* tail, ElemType e) {
    Node *p = (Node*)malloc(sizeof(Node));
    p -> data = e;
    tail -> next = p;
    p -> next = NULL;
    return p;
}//尾插入

Node* insertMiddle (Node* L, int position, ElemType e) {
    Node *p = L;
    int i = 0;
    while(i < position - 1) {
        p = p -> next;
        i++;
        if (p == NULL) {
            return 0;
        }
    }

    Node *q = (Node*)malloc(sizeof(Node));
    q -> data = e;
    q -> next = p -> next;
    p -> next = q;
    return q;
}//中间插入法

int deleteNode (Node *L, int position) {
    Node *p = L;
    int i = 0;
    while (i < position - 1) {
        p = p -> next;
        i++;
        if (p == NULL) {
            return 0;
        }
    }

    if (p -> next == NULL) {
        printf("The Delete Position is Error");
        return 0;
    }

    Node *q  = p -> next;
    p -> next = q -> next;
    free(q);
    return 1;
}//删除节点

int listLength (Node *L) {
    Node *p = L;
    int len = 0;
    while (p != NULL) {
        p = p -> next;
        len++;
    }

    return len;
}//计算链表长度

void freeList (Node *L) {
    Node *p = L -> next;
    Node *q;

    while (p != NULL) {
        q = p -> next;
        free(p);
        p = q;
    }

    L -> next = NULL;
}


int main() {
    Node *list = initList();
    insertHead(list, 10);
    insertHead(list, 20);
    insertHead(list, 11);
    Node *tail = get_tail(list);
    tail = insertTail(tail, 90);
    tail = insertTail(tail, 100);
    listNode(list);
    insertMiddle(list, 2, 40);
    listNode(list);
    deleteNode(list, 2);
    listNode(list);
    printf("The list length is %d\n", listLength(list));
    freeList(list);
    printf("The list length is %d\n", listLength(list));
    return 1;
}
