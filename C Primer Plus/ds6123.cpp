#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int val;
    struct ListNode *next;
} ListNode;

ListNode* createList() {
    ListNode *head = (ListNode*)malloc(sizeof(ListNode));
    head->next = NULL;
    return head;
}

void insertHead(ListNode *head, int e) {
    ListNode *newNode = (ListNode*)malloc(sizeof(ListNode));
    newNode->val = e;
    newNode->next = head->next;
    head->next = newNode;
}

void printList(ListNode *head) {
    ListNode *p = head->next;
    while (p != NULL) {
        printf("\t%d", p->val);
        if (p->next != NULL) {
            printf(" ");
        }
        p = p->next;
    }
    printf("\n");
}

int isInList(ListNode *head, int x) {
    ListNode *p = head->next;
    while (p != NULL) {
        if (p->val == x) {
            return 1;
        }
        p = p->next;
    }
    return 0;
}

void partitionList(ListNode *head, int x) {
    ListNode *lessHead = createList();
    ListNode *greaterHead = createList();
    ListNode *xNode = NULL;
    ListNode *p = head->next;
    ListNode *lessTail = lessHead;
    ListNode *greaterTail = greaterHead;
    
    while (p != NULL) {
        if (p->val < x) {
            lessTail->next = p;
            lessTail = lessTail->next;
        } else if (p->val > x) {
            greaterTail->next = p;
            greaterTail = greaterTail->next;
        } else {
            xNode = p;
        }
        p = p->next;
    }

    if (xNode != NULL) {
        lessTail->next = xNode;
        xNode->next = greaterHead->next;
        greaterTail->next = NULL;
    } else {
        lessTail->next = greaterHead->next;
        greaterTail->next = NULL;
    }

    head->next = lessHead->next;
    free(lessHead);
    free(greaterHead);
}

void destroyList(ListNode *head) {
    ListNode *p = head->next;
    while (p != NULL) {
        ListNode *temp = p;
        p = p->next;
        free(temp);
    }
    free(head);
}

int main() {
    ListNode *head = createList();
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