#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char data;
    struct Node* next;
} Node;

Node* createNode(char ch) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (newNode == NULL) {
        exit(1);
    }
    newNode->data = ch;
    newNode->next = NULL;
    return newNode;
}

Node* stringToList(const char* str) {
    if (str == NULL || *str == '\0') {
        return NULL;
    }
    
    Node* head = createNode(*str);
    Node* current = head;
    
    for (int i = 1; str[i] != '\0'; i++) {
        current->next = createNode(str[i]);
        current = current->next;
    }
    
    return head;
}

void freeList(Node* head) {
    Node* temp;
    while (head != NULL) {
        temp = head;
        head = head->next;
        free(temp);
    }
}

void printList(Node* head) {
    while (head != NULL) {
        printf("%c", head->data);
        head = head->next;
    }
    printf("\n");
}

Node* findSubstring(Node* s, Node* r) {
    if (r == NULL) return s;
    
    Node* s_ptr = s;
    Node* r_ptr = r;
    Node* potential_start = NULL;
    
    while (s_ptr != NULL) {
        Node* s_temp = s_ptr;
        Node* r_temp = r_ptr;
        potential_start = s_ptr;
        
        while (s_temp != NULL && r_temp != NULL && s_temp->data == r_temp->data) {
            s_temp = s_temp->next;
            r_temp = r_temp->next;
        }
        
        if (r_temp == NULL) {
            return potential_start;
        }
        
        s_ptr = s_ptr->next;
    }
    
    return NULL;
}

Node* replaceSubstring(Node* s, Node* r, Node* t) {
    if (s == NULL || r == NULL) return s;

    Node* match_start = findSubstring(s, r);
    if (match_start == NULL) return NULL;

    int r_len = 0;
    Node* r_ptr = r;
    while (r_ptr != NULL) {
        r_len++;
        r_ptr = r_ptr->next;
    }

    Node* t_copy = NULL;
    Node* t_tail = NULL;
    Node* t_ptr = t;
    while (t_ptr != NULL) {
        Node* newNode = createNode(t_ptr->data);
        if (t_copy == NULL) {
            t_copy = t_tail = newNode;
        } else {
            t_tail->next = newNode;
            t_tail = newNode;
        }
        t_ptr = t_ptr->next;
    }

    if (s == match_start) {
        Node* r_end = s;
        for (int i = 0; i < r_len && r_end != NULL; i++) {
            r_end = r_end->next;
        }

        if (t_tail != NULL) {
            t_tail->next = r_end;
        } else {
            t_copy = r_end;
        }

        Node* to_free = s;
        for (int i = 0; i < r_len && to_free != NULL; i++) {
            Node* temp = to_free;
            to_free = to_free->next;
            free(temp);
        }
        
        return t_copy ? t_copy : r_end;
    }

    Node* prev = s;
    while (prev->next != match_start) {
        prev = prev->next;
    }

    Node* r_end = match_start;
    for (int i = 0; i < r_len && r_end != NULL; i++) {
        r_end = r_end->next;
    }

    if (t_tail != NULL) {
        t_tail->next = r_end;
    }

    prev->next = t_copy ? t_copy : r_end;

    Node* to_free = match_start;
    for (int i = 0; i < r_len && to_free != NULL; i++) {
        Node* temp = to_free;
        to_free = to_free->next;
        free(temp);
    }
    
    return s;
}

int main() {
    char s[1000], r[1000], t[1000];

    fgets(s, sizeof(s), stdin);
    fgets(r, sizeof(r), stdin);
    fgets(t, sizeof(t), stdin);

    s[strcspn(s, "\n")] = '\0';
    r[strcspn(r, "\n")] = '\0';
    t[strcspn(t, "\n")] = '\0';

    Node* s_list = stringToList(s);
    Node* r_list = stringToList(r);
    Node* t_list = stringToList(t);

    Node* result = replaceSubstring(s_list, r_list, t_list);
    
    if (result != NULL) {
        printList(result);
    } else {
        printf("NONE\n");
    }
    
    freeList(result);
    freeList(r_list);
    freeList(t_list);
    
    return 0;
}