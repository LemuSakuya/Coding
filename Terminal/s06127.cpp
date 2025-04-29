#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 20

typedef struct {
    int data[MAX_SIZE];
    int front, rear;
} Queue;

void initQueue(Queue *q) {
    q->front = q->rear = 0;
}

int isEmpty(Queue *q) {
    return q->front == q->rear;
}

int isFull(Queue *q) {
    return (q->rear + 1) % MAX_SIZE == q->front;
}

void enqueue(Queue *q, int value) {
    if (isFull(q)) {
        return;
    }
    q->data[q->rear] = value;
    q->rear = (q->rear + 1) % MAX_SIZE;
}

int dequeue(Queue *q) {
    if (isEmpty(q)) {
        return -1;
    }
    int value = q->data[q->front];
    q->front = (q->front + 1) % MAX_SIZE;
    return value;
}

int main() {
    int n, m;
    scanf("%d%d", &n, &m);
    
    if (n <= 0 || n >= 20 || m <= 0 || m > n) {
        printf("ERROR");
        return 0;
    }
    
    Queue q;
    initQueue(&q);
    
    for (int i = 1; i <= n; i++) {
        enqueue(&q, i);
    }
    
    while (!isEmpty(&q)) {
        for (int i = 1; i < m; i++) {
            int person = dequeue(&q);
            enqueue(&q, person);
        }
        int out = dequeue(&q);
        printf("\t%d", out);
    }
    
    return 0;
}