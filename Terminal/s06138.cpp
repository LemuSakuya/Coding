#include <bits/stdc++.h>
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
        if (index >= s.length() || s[index] == ')') {
            index++;
            return NULL;
        }

        if (s[index] == ',') {
            index++;
            return buildTree(s, index);
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

    void preOrder(TreeNode* node, string& result) {
        if (!node) return;
        result += node->data;
        preOrder(node->left, result);
        preOrder(node->right, result);
    }

    void postOrder(TreeNode* node, string& result) {
        if (!node) return;
        postOrder(node->left, result);
        postOrder(node->right, result);
        result += node->data;
    }

    void levelOrder(TreeNode* node, string& result) {
        if (!node) return;
        queue<TreeNode*> q;
        q.push(node);
        while (!q.empty()) {
            TreeNode* current = q.front();
            q.pop();
            result += current->data;
            if (current->left) q.push(current->left);
            if (current->right) q.push(current->right);
        }
    }

    void treeToString(TreeNode* node, string& result) {
        if (!node) return;
        result += node->data;
        if (node->left || node->right) {
            result += '(';
            if (node->left) {
                treeToString(node->left, result);
            }
            if (node->right) {
                result += ',';
                treeToString(node->right, result);
            }
            result += ')';
        }
    }

public:
    BinaryTree() : root(NULL) {}
    ~BinaryTree() { destroyTree(root); }

    void createTree(const string& s) {
        int index = 0;
        root = new TreeNode(s[index++]);
        
        if (index < s.length() && s[index] == '(') {
            index++;

            root->left = buildTree(s, index);
            
            if (index < s.length() && s[index] == ',') {
                index++;
                root->right = buildTree(s, index);
            }

            if (index < s.length() && s[index] == ')') {
                index++;
            }
        }
        
        while (index < s.length() && s[index] == ',') {
            index++;
            TreeNode* sibling = buildTree(s, index);

            TreeNode* newRoot = new TreeNode(root->data);
            newRoot->left = root;
            newRoot->right = sibling;
            root = newRoot;
        }
    }

    string getTreeString() {
        string result;
        treeToString(root, result);
        return result;
    }

    int depth() {
        return getDepth(root);
    }

    string preOrderTraversal() {
        string result;
        preOrder(root, result);
        return result;
    }

    string postOrderTraversal() {
        string result;
        postOrder(root, result);
        return result;
    }

    string levelOrderTraversal() {
        string result;
        levelOrder(root, result);
        return result;
    }
};

int main() {
    string input;
    getline(cin, input);

    BinaryTree tree;
    tree.createTree(input);

    cout << "BT:" << input << endl;
    cout << "depth:" << tree.depth() << endl;
    cout << "preorder:" << tree.preOrderTraversal() << endl;
    cout << "postorder:" << tree.postOrderTraversal() << endl;
    cout << "levelorder:" << tree.levelOrderTraversal() << endl;

    return 0;
}