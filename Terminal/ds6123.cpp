#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int val;
    struct Node *next;
} Node;

Node* createList() {
    Node *head = (Node*)malloc(sizeof(Node));
    head->next = NULL;
    return head;
}

void insertHead(Node *head, int e) {
    Node *newNode = (Node*)malloc(sizeof(Node));
    newNode->val = e;
    newNode->next = head->next;
    head->next = newNode;
}

void printList(Node *head) {
    Node *p = head->next;
    while (p != NULL) {
        printf("\t%d", p->val);
        p = p->next;
        if (p != NULL) {
            printf(" ");
        }
    }
    printf("\n");
}

int isInList(Node *head, int x) {
    Node *p = head->next;
    while (p != NULL) {
        if (p->val == x) {
            return 1;
        }
        p = p->next;
    }
    return 0;
}

void partitionList(Node *head, int x) {
    Node lessHead = {0, NULL};  // 小于x的链表头
    Node greaterHead = {0, NULL};  // 大于x的链表头
    Node *xNode = NULL;  // x节点
    Node *lessTail = &lessHead;
    Node *greaterTail = &greaterHead;
    
    Node *p = head->next;
    while (p != NULL) {
        Node *next = p->next;
        if (p->val < x) {
            lessTail->next = p;
            lessTail = lessTail->next;
        } else if (p->val > x) {
            greaterTail->next = p;
            greaterTail = greaterTail->next;
        } else {
            xNode = p;
        }
        p = next;
    }

    // 连接三个部分
    if (xNode != NULL) {
        lessTail->next = xNode;
        xNode->next = greaterHead.next;
        greaterTail->next = NULL;
    } else {
        lessTail->next = greaterHead.next;
        greaterTail->next = NULL;
    }

    head->next = lessHead.next;
}

void destroyList(Node *head) {
    Node *p = head->next;
    while (p != NULL) {
        Node *temp = p;
        p = p->next;
        free(temp);
    }
    free(head);
}

int main() {
    Node *head = createList();
    int n, e, x;

    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        scanf("%d", &e);
        insertHead(head, e);
    }

    printList(head);

    scanf("%d", &x);

    if (!isInList(head, x)) {
        printf("ERROR input\n");
    } else {
        partitionList(head, x);
        printList(head);
    }

    destroyList(head);

    return 0;
}