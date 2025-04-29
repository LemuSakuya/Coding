#include <bits/stdc++.h>
using namespace std;

int precedence(char op);
void infixToPostfix(char* expstr, char* postexp);
int evaluatePostfix(char* postexp);

int main() {
    char expstr[100];
    char postexp[200] = {0};
    int value;
    
    scanf("%s", expstr);
    

    infixToPostfix(expstr, postexp);
    printf("postexp:%s\n", postexp);
    
    try {
        value = evaluatePostfix(postexp);
        printf("value:%d\n", value);
    } catch (const char* msg) {
        if (strcmp(msg, "Divide by 0") == 0) {
            printf("Divide by 0\n");
        }
    }
    
    return 0;
}

int precedence(char op) {
    if (op == '+' || op == '-') {
        return 1;
    } else if (op == '*' || op == '/') {
        return 2;
    }
    return 0;
}

void infixToPostfix(char* expstr, char* postexp) {
    stack<char> s;
    int postIndex = 0;
    int i = 0;
    
    while (expstr[i] != '\0') {
        if (isdigit(expstr[i])) {
            while (isdigit(expstr[i])) {
                postexp[postIndex++] = expstr[i++];
            }
            postexp[postIndex++] = '#';
        } else if (expstr[i] == '(') {
            s.push(expstr[i]);
            i++;
        } else if (expstr[i] == ')') {
            while (!s.empty() && s.top() != '(') {
                postexp[postIndex++] = s.top();
                s.pop();
            }
            s.pop();
            i++;
        } else {
            while (!s.empty() && precedence(expstr[i]) <= precedence(s.top())) {
                postexp[postIndex++] = s.top();
                s.pop();
            }
            s.push(expstr[i]);
            i++;
        }
    }

    while (!s.empty()) {
        postexp[postIndex++] = s.top();
        s.pop();
    }
    
    postexp[postIndex] = '\0';
}

int evaluatePostfix(char* postexp) {
    stack<int> s;
    int i = 0;
    
    while (postexp[i] != '\0') {
        if (isdigit(postexp[i])) {

            int num = 0;
            while (isdigit(postexp[i])) {
                num = num * 10 + (postexp[i] - '0');
                i++;
            }
            s.push(num);
            i++;
        } else {
            int val2 = s.top(); s.pop();
            int val1 = s.top(); s.pop();
            
            switch (postexp[i]) {
                case '+': s.push(val1 + val2); break;
                case '-': s.push(val1 - val2); break;
                case '*': s.push(val1 * val2); break;
                case '/': 
                    if (val2 == 0) {
                        throw "Divide by 0";
                    }
                    s.push(val1 / val2); 
                    break;
            }
            i++;
        }
    }
    
    return s.top();
}