#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
using namespace std;

void dfs(const vector<vector<int>>& adjList, int v, vector<bool>& visited, vector<int>& result) {
    visited[v] = true;
    result.push_back(v);
    for (int neighbor : adjList[v]) {
        if (!visited[neighbor]) {
            dfs(adjList, neighbor, visited, result);
        }
    }
}

void bfs(const vector<vector<int>>& adjList, int start, vector<int>& result) {
    vector<bool> visited(adjList.size(), false);
    queue<int> q;
    q.push(start);
    visited[start] = true;
    
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        result.push_back(v);
        
        for (int neighbor : adjList[v]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}

int main() {
    int n;
    cin >> n;
    
    vector<vector<int>> adjMatrix(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        string row;
        cin >> row;
        for (int j = 0; j < n; ++j) {
            adjMatrix[i][j] = row[j] - '0';
        }
    }
    
    int dfsStart, bfsStart;
    cin >> dfsStart >> bfsStart;
    
    // 创建邻接表并按编号从小到大排序
    vector<vector<int>> adjList(n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (adjMatrix[i][j] == 1) {
                adjList[i].push_back(j);
            }
        }
        sort(adjList[i].begin(), adjList[i].end());
    }
    
    // 输出邻接表
    for (int i = 0; i < n; ++i) {
        cout << i << ":";
        for (int neighbor : adjList[i]) {
            cout << neighbor;
        }
        cout << endl;
    }
    
    // DFS遍历
    vector<bool> visited(n, false);
    vector<int> dfsResult;
    dfs(adjList, dfsStart, visited, dfsResult);
    cout << "DFS:";
    for (int v : dfsResult) {
        cout << v;
    }
    cout << endl;
    
    // BFS遍历
    vector<int> bfsResult;
    bfs(adjList, bfsStart, bfsResult);
    cout << "BFS:";
    for (int v : bfsResult) {
        cout << v;
    }
    cout << endl;
    
    return 0;
}