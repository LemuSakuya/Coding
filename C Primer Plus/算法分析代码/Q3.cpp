#include <bits/stdc++.h>
using namespace std;

typedef int ElemType;

typedef struct node {
    ElemType data;
    struct node *next;
} Node;

Node* initList() {
    Node *head = (Node*)malloc(sizeof(Node));
    head->data = 0;  // 头节点数据域不使用
    head->next = NULL;
    return head;
}

void insertTail(Node *head, ElemType data) {
    Node *p = (Node*)malloc(sizeof(Node));
    p->data = data;
    p->next = NULL;
    if (head->next == NULL) {
        head->next = p;
    } else {
        Node *q = head->next;
        while (q->next != NULL) {
            q = q->next;
        }
        q->next = p;
    }
}

void insertHead(Node *head, ElemType data) {
    Node *p = (Node*)malloc(sizeof(Node));
    p->data = data;
    p->next = head->next;
    head->next = p;
}

void checkNode(Node *head) {
    if (head == NULL || head->next == NULL) {
        return;  // 空链表或只有头节点，无需处理
    }

    unordered_set<int> seen_abs;  // 记录已出现的绝对值
    Node *prev = head;            // 前驱指针（初始指向头节点）
    Node *curr = head->next;      // 当前指针（初始指向第一个有效节点）

    while (curr != NULL) {
        int abs_val = abs(curr->data);

        if (seen_abs.find(abs_val) == seen_abs.end()) {
            // 当前绝对值未出现过，保留节点并更新前驱指针
            seen_abs.insert(abs_val);
            prev = curr;
            curr = curr->next;
        } else {
            // 当前绝对值已出现过，删除节点
            prev->next = curr->next;
            Node *temp = curr;
            curr = curr->next;
            free(temp);
        }
    }
}

void listprint(Node *head) {
    Node *p = head->next;  // 跳过头节点
    while (p != NULL) {
        printf("%d\t", p->data);
        p = p->next;
    }
    printf("\n");
}

int main() {
    Node *head = initList();
    insertTail(head, -1);
    insertTail(head, 2);
    insertTail(head, 2);
    insertTail(head, -2);
    insertTail(head, -6);
    insertTail(head, 4);
    insertTail(head, 5);
    insertTail(head, -3);
    insertTail(head, 4);
    insertTail(head, 9);
    insertTail(head, -3);
    insertTail(head, 8);
    listprint(head);
    checkNode(head);
    listprint(head);
    return 0;
}