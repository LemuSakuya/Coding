#include <stdio.h>
#include <stdlib.h>

typedef char ElemType;

typedef struct node {
    ElemType data;
    struct node *next;
} Node;

Node* initList() {
    Node *p = (Node*)malloc(sizeof(Node));
    p->data = 0;    // 头节点数据域不使用
    p->next = NULL;
    return p;
}

Node* get_tail(Node *L) {
    Node *p = L;
    while (p->next != NULL) {
        p = p->next;
    }
    return p;
}

Node* insertTail(Node *L, ElemType c) {
    Node *tail = get_tail(L);
    
    Node *newNode = (Node*)malloc(sizeof(Node));
    newNode->data = c;
    newNode->next = NULL;
    
    tail->next = newNode;
    
    return newNode;
}

void listprint(Node *L) {
    Node *p = L->next;  // 跳过头节点
    while (p != NULL) {
        printf("%c\t", p->data);
        p = p->next;
    }
    printf("\n");
}

int main() {
    Node *listA = initList();
    Node *listB = initList();

    insertTail(listA, 'l');
    insertTail(listA, 'o');
    insertTail(listA, 'a');
    insertTail(listA, 'd');

    insertTail(listB, 'b');
    insertTail(listB, 'e');

    printf("List A: ");
    listprint(listA);  // 应该输出: l   o   a   d
    
    printf("List B: ");
    listprint(listB);  // 应该输出: b   e

    return 0;
}