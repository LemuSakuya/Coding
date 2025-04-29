#include <bits/stdc++.h>
using namespace std;

struct Triple {
    int row;
    int col;
    int data;

    bool operator<(const Triple& other) const {
        if (row != other.row) return row < other.row;
        return col < other.col;
    }
};

class SparseMatrix {
private:
    int rows, cols;
    vector<Triple> elements;

    vector<Triple>::iterator find_position(int row, int col) {
        Triple temp = {row, col, 0};
        return lower_bound(elements.begin(), elements.end(), temp);
    }

public:
    SparseMatrix(int m, int n) : rows(m), cols(n) {}

    bool insert(int row, int col, int x) {
        if (row < 0 || row >= rows || col < 0 || col >= cols) {
            printf("Value ERROR\n");
            return false;
        }
        
        if (x == 0) {

            for (vector<Triple>::iterator it = elements.begin(); it != elements.end(); ++it) {
                if (it->row == row && it->col == col) {
                    elements.erase(it);
                    return true;
                }
            }
            return true;
        }

        vector<Triple>::iterator pos = find_position(row, col);

        if (pos != elements.end() && pos->row == row && pos->col == col) {
            pos->data = x;
            return true;
        }
        
        Triple t = {row, col, x};
        elements.insert(pos, t);
        return true;
    }

    int get(int row, int col) {
        if (row < 0 || row >= rows || col < 0 || col >= cols) {
            printf("Assign ERROR\n");
            return -1;
        }
        
        Triple temp = {row, col, 0};
        vector<Triple>::iterator pos = lower_bound(elements.begin(), elements.end(), temp);
        
        if (pos != elements.end() && pos->row == row && pos->col == col) {
            return pos->data;
        }
        
        return 0;
    }

    void printTriples() {
        printf("rows=%d\tcols=%d\tnums=%d\n", rows, cols, (int)elements.size());
        for (size_t i = 0; i < elements.size(); i++) {
            printf("%d\t%d\t%d\n", elements[i].row, elements[i].col, elements[i].data);
        }
    }
};

int main() {
    int m, n;
    scanf("%d%d", &m, &n);
    
    SparseMatrix matrix(m, n);

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            int val;
            scanf("%d", &val);
            if (val != 0) {
                matrix.insert(i, j, val);
            }
        }
    }

    matrix.printTriples();

    int op;
    while (scanf("%d", &op) == 1) {
        if (op == 1) {

            int row, col, x;
            scanf("%d%d%d", &row, &col, &x);
            bool success = matrix.insert(row, col, x);
            if (success) {
                matrix.printTriples();
            }
        } else if (op == 2) {

            int row, col;
            scanf("%d%d", &row, &col);
            int val = matrix.get(row, col);
            if (val != -1) {
                printf("A[%d][%d]=%d\n", row, col, val);
            }
        } else {
            break;
        }
    }
    
    return 0;
}