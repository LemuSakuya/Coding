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

void insertOrder(ListNode *head, int e) {
    ListNode *p = head;
    while (p->next != NULL && p->next->val < e) {
        p = p->next;
    }
    if (p->next != NULL && p->next->val == e) {
        return;
    }
    ListNode *newNode = (ListNode*)malloc(sizeof(ListNode));
    newNode->val = e;
    newNode->next = p->next;
    p->next = newNode;
}

void inputList(ListNode *head) {
    int m;
    while (1) {
        scanf("%d", &m);
        if (m == -1) break;
        if (m > 0) {
            insertOrder(head, m);
        }
    }
}

void printList(ListNode *head, const char *prefix) {
    printf("%s-->", prefix);
    if (head->next == NULL) {
        printf("none\n");
        return;
    }
    ListNode *p = head->next;
    while (p != NULL) {
        printf("%d", p->val);
        if (p->next != NULL) {
            printf("\t");
        }
        p = p->next;
    }
    printf("\n");
}

ListNode* copyList(ListNode *src) {
    ListNode *dest = createList();
    ListNode *p = src->next;
    while (p != NULL) {
        insertOrder(dest, p->val);
        p = p->next;
    }
    return dest;
}

ListNode* unionList(ListNode *L1, ListNode *L2) {
    ListNode *L3 = createList();
    ListNode *p1 = L1->next, *p2 = L2->next;
    while (p1 != NULL && p2 != NULL) {
        if (p1->val < p2->val) {
            insertOrder(L3, p1->val);
            p1 = p1->next;
        } else if (p1->val > p2->val) {
            insertOrder(L3, p2->val);
            p2 = p2->next;
        } else {
            insertOrder(L3, p1->val);
            p1 = p1->next;
            p2 = p2->next;
        }
    }
    while (p1 != NULL) {
        insertOrder(L3, p1->val);
        p1 = p1->next;
    }
    while (p2 != NULL) {
        insertOrder(L3, p2->val);
        p2 = p2->next;
    }
    return L3;
}

ListNode* intersectList(ListNode *L1, ListNode *L2) {
    ListNode *L4 = createList();
    ListNode *p1 = L1->next, *p2 = L2->next;
    while (p1 != NULL && p2 != NULL) {
        if (p1->val < p2->val) {
            p1 = p1->next;
        } else if (p1->val > p2->val) {
            p2 = p2->next;
        } else {
            insertOrder(L4, p1->val);
            p1 = p1->next;
            p2 = p2->next;
        }
    }
    return L4;
}

ListNode* diffList(ListNode *L1, ListNode *L2) {
    ListNode *L5 = createList();
    ListNode *p1 = L1->next, *p2 = L2->next;
    while (p1 != NULL && p2 != NULL) {
        if (p1->val < p2->val) {
            insertOrder(L5, p1->val);
            p1 = p1->next;
        } else if (p1->val > p2->val) {
            p2 = p2->next;
        } else {
            p1 = p1->next;
            p2 = p2->next;
        }
    }
    while (p1 != NULL) {
        insertOrder(L5, p1->val);
        p1 = p1->next;
    }
    return L5;
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
    ListNode *L1 = createList();
    ListNode *L2 = createList();

    inputList(L1);
    inputList(L2);

    // 输出原始链表
    printList(L1, "L1");
    printList(L2, "L2");

    ListNode *L3 = unionList(L1, L2);
    ListNode *L4 = intersectList(L1, L2);
    ListNode *L5 = diffList(L1, L2);

    printList(L3, "L3");
    printList(L4, "L4");
    printList(L5, "L5");

    destroyList(L1);
    destroyList(L2);
    destroyList(L3);
    destroyList(L4);
    destroyList(L5);

    return 0;
}