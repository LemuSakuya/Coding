#include <bits/stdc++.h>

typedef int ElemType;

typedef struct node {
    ElemType data;
    struct node *next;
} Node;

Node* initList () {
    Node *head = (Node*)malloc(sizeof(Node));
    head -> data = 0;
    head -> next = NULL;
    return head;
}

int insertHead (Node *L, ElemType d) {
    Node *p = (Node*)malloc(sizeof(Node));
    p -> data = d;
    p -> next = L -> next;
    L -> next = p;
    return 1;
}

void listprint (Node *L) {
    Node *p = L -> next;
    while (p != NULL) {
        printf("%d\t", p -> data);
        p = p -> next;
    }
    printf ("\n");
}

void findNodeFS (Node *L, int k) {
    Node *fast = L -> next;
    Node *slow = L -> next;
    Node *count = L -> next;
    int length = 0;

    while (count -> next != NULL) {
        length++;
        count = count -> next;
    }

    if (k > length) {
        printf("Your find Node is not exsist\n");
    }

    for (int i = 0; i < k; i++) {
        fast = fast -> next;
    }

    while (fast != NULL) {
        fast = fast -> next;
        slow = slow -> next;
    }

    printf("The number is %d, and it's data is %d\n", k, slow -> data);
}

int main () {
    Node* list = initList();
    insertHead(list, 1);
    insertHead(list, 2);
    insertHead(list, 3);
    insertHead(list, 4);
    insertHead(list, 5);
    listprint(list);
    findNodeFS(list, 2);
    findNodeFS(list, 10);
    return 0;

}