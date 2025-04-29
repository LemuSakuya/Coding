#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct TreeNode {
    char data;
    TreeNode* left;
    TreeNode* right;
    TreeNode(char val) : data(val), left(NULL), right(NULL) {}
};

class BinaryTree {
private:
    TreeNode* root;

    TreeNode* buildTree(const string& s, int& index) {
        if (index >= s.length() || s[index] == ')' || s[index] == '.') {
            if (s[index] == '.') index++;
            index++;
            return NULL;
        }

        TreeNode* node = new TreeNode(s[index++]);
        
        if (index < s.length() && s[index] == '(') {
            index++;
            node->left = buildTree(s, index);
            if (index < s.length() && s[index] == ',') {
                index++;
                node->right = buildTree(s, index);
            }
            if (index < s.length() && s[index] == ')') {
                index++;
            }
        }
        return node;
    }

    void destroyTree(TreeNode* node) {
        if (node) {
            destroyTree(node->left);
            destroyTree(node->right);
            delete node;
        }
    }

    int getDepth(TreeNode* node) {
        if (!node) return 0;
        return max(getDepth(node->left), getDepth(node->right)) + 1;
    }

    void findLeafPaths(TreeNode* node, vector<char>& path, vector<vector<char> >& allPaths) {
        if (!node) return;

        path.push_back(node->data);

        if (!node->left && !node->right) {
            allPaths.push_back(path);
        } else {
            findLeafPaths(node->left, path, allPaths);
            findLeafPaths(node->right, path, allPaths);
        }

        path.pop_back();
    }

public:
    BinaryTree() : root(NULL) {}
    ~BinaryTree() { destroyTree(root); }

    void createTree(const string& s) {
        int index = 0;
        root = buildTree(s, index);
    }

    vector<vector<char> > getAllLeafPaths() {
        vector<vector<char> > allPaths;
        vector<char> path;
        findLeafPaths(root, path, allPaths);
        return allPaths;
    }

    int depth() {
        return getDepth(root);
    }
};

int main() {
    string input;
    cin >> input;

    BinaryTree tree;
    tree.createTree(input);

    vector<vector<char> > paths = tree.getAllLeafPaths();
    for (const auto& path : paths) {
        for (int i = 0; i < path.size(); i++) {
            cout << path[i];
            if (i != path.size() - 1) {
                cout << "->";
            }
        }
        cout << endl;
    }

    cout << "Depth:" << tree.depth() << endl;

    return 0;
}