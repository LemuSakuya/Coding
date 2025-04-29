#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

void createAdjList(vector<vector<int>>& adjList, const vector<vector<int>>& matrix, int n);
void printAdjList(const vector<vector<int>>& adjList);
void DFS(const vector<vector<int>>& adjList, int start, vector<bool>& visited, vector<int>& result);
void BFS(const vector<vector<int>>& adjList, int start, vector<bool>& visited, vector<int>& result);

int main() {
    int n;
    cin >> n;

    vector<vector<int>> matrix(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            cin >> matrix[i][j];
        }
    }

    vector<vector<int>> adjList(n);
    createAdjList(adjList, matrix, n);

    printAdjList(adjList);

    int dfsStart, bfsStart;
    cin >> dfsStart >> bfsStart;

    vector<bool> visited(n, false);
    vector<int> dfsResult;
    DFS(adjList, dfsStart, visited, dfsResult);

    cout << "DFS：";
    for (size_t i = 0; i < dfsResult.size(); ++i) {
        if (i != 0) cout << " ";
        cout << dfsResult[i];
    }
    cout << endl;

    fill(visited.begin(), visited.end(), false);
    vector<int> bfsResult;
    BFS(adjList, bfsStart, visited, bfsResult);

    cout << "BFS：";
    for (size_t i = 0; i < bfsResult.size(); ++i) {
        if (i != 0) cout << " ";
        cout << bfsResult[i];
    }
    cout << endl;
    
    return 0;
}

void createAdjList(vector<vector<int>>& adjList, const vector<vector<int>>& matrix, int n) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (matrix[i][j] == 1) {
                adjList[i].push_back(j);
            }
        }

        sort(adjList[i].begin(), adjList[i].end());
    }
}

void printAdjList(const vector<vector<int>>& adjList) {
    for (size_t i = 0; i < adjList.size(); ++i) {
        cout << i << "：";
        for (size_t j = 0; j < adjList[i].size(); ++j) {
            if (j != 0) cout << " ";
            cout << adjList[i][j];
        }
        cout << endl;
    }
}

void DFS(const vector<vector<int>>& adjList, int start, vector<bool>& visited, vector<int>& result) {
    visited[start] = true;
    result.push_back(start);
    
    for (int neighbor : adjList[start]) {
        if (!visited[neighbor]) {
            DFS(adjList, neighbor, visited, result);
        }
    }
}

void BFS(const vector<vector<int>>& adjList, int start, vector<bool>& visited, vector<int>& result) {
    queue<int> q;
    q.push(start);
    visited[start] = true;
    
    while (!q.empty()) {
        int current = q.front();
        q.pop();
        result.push_back(current);
        
        for (int neighbor : adjList[current]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}