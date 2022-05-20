#include<iostream>
using namespace std;
//--------------------------------------- Tree Class ----------------------------------------------------------//
class Tree {
    friend ostream& operator<<(ostream& os, Tree& tree); // ostream operator which prints the parent array
protected:
    int* parentArray; // The parentArray that stores the parents of node i
    int _size; // Thesize of the parentArray
public:
    Tree(); // Default Constructor
    Tree(int size); // Non-Default constructor
    Tree(Tree & anotherTree); // Copy Constructor
    ~Tree(); //Destructor
    int getSize(); // Get the size of the parentArray
    int* getParentArray(); // Get the parentArray
    int LCA(int firstNode, int secondNode); // Returns the least common ancestor given two nodes
    int parent(int i); // Get the parent of node i
    void children(int i); // Prints the children of node i
    void siblings(int i); // Prints the siblings of node i
    int root(); // Get the root of the tree
    void setRoot(int rootNode); // Set the root of the tree
    void setParent(int node, int parent); // Set the parent of the node
    void nodesAtLevel(int i); // Print the nodes at level i
    int level(int i); // Get the level of node i
    int height(); // Get the hight of the tree
    void preorder(int i); // Give the Preorder traversal of the tree
};
//methods
Tree::Tree() {
    _size = 0;
    parentArray = NULL;
}
Tree::Tree(int size) {
    _size = size;
    parentArray = new int[size];
    for (int i = 0; i < size; i++) {
        parentArray[i] = -1;
    }
}
Tree::Tree(Tree& anotherTree) {
    _size = anotherTree.getSize();
    parentArray = new int[anotherTree.getSize()];
    for (int i = 0; i < anotherTree.getSize(); i++) {
        parentArray[i] = anotherTree.parent(i);
    }
}
Tree::~Tree() {
    delete[] parentArray;
}
int Tree::getSize() {
    return _size;
}
int* Tree::getParentArray() {
    return parentArray;
}
int Tree::LCA(int firstNode, int secondNode) {
    int currentNode = firstNode;
    int nodeStep = secondNode;
    bool LCA_found = false;
    while (!LCA_found){
        if (currentNode == secondNode) {
            LCA_found = true;
        }
        for (int i = 0; i < this->level(secondNode); i++) {
            nodeStep = this->parent(nodeStep);
            if (nodeStep == currentNode) {
                LCA_found = true;
                break;
            }
        }
        if (!LCA_found) {
            currentNode = this->parent(currentNode);
            nodeStep = secondNode;
        }
    }
    return currentNode;
}
int Tree::parent(int i) {
    return parentArray[i];
}
void Tree::children(int i) {
    for (int j = 0; j < _size; j++) {
        if (this->parent(j) == i) {
            cout << j << " ";
        }
    }
    cout << endl;
}
void Tree::siblings(int i) {
    int parent;
    parent = this->parent(i);
    for (int j = 0; j < _size; j++) {
        if (this->parent(j) == parent && j != i) {
            cout << j << " ";
        }
    }
    cout << endl;
}
int Tree::root() {
    int index = 0;
    for (int i = 0; i < _size; i++) {
        if (parentArray[i] == -1) {
            break;
        }
        index++;
    }
    return index;
}
void Tree::setRoot(int i) {
    parentArray[i] = -1;
}
void Tree::setParent(int node, int parent) {
    parentArray[node] = parent;
}
void Tree::nodesAtLevel(int i) {
    cout << "Nodes at level " << i << ":" << endl;
    for (int j = 0; j < _size; j++) {
        if (this->level(j) == i) {
            cout << j << " ";
        }
    }
    cout << endl;
}
int Tree::level(int i) {
    int parent = 0;
    int counter = 0;
    while (parent != -1) {
        parent = this->parent(i);
        i = parent;
        counter++;
    }
    return counter;
}
int Tree::height() {
    int tree_height = 0;
    for (int i = 0; i < _size; i++) {
        if (this->level(i) > tree_height) {
            tree_height = this->level(i);
        }
    }
    return tree_height;
}
void Tree::preorder(int i) {
    for (int j = 0; j < _size; j++) {
        if (this->parent(j) == i) {
            cout << j << " ";
            this->preorder(j);
        }
    }
}
//ostream oper
ostream& operator<<(ostream& os, Tree& tree) {
    for (int i = 0; i < tree._size; i++) {
        os << i << ": " << tree.parent(i) << "    ";
    }
    os << endl;
    return os;
}
//--------------------------------------------- main function --------------------------------------------------//
int main()
{
    int numNodes, numChildren, nodeNum, childNum; // you may use these or not
    // read in the number of nodes in the tree
    cin >> numNodes;
    // create object of class Tree
    Tree* myTree = new Tree(numNodes);
    // read in the information about each node and build the parent array 
    for (int i = 0; i < numNodes; i++) {
        cin >> nodeNum;
        cin >> numChildren;
        for (int j = 0; j < numChildren; j++) {
            cin >> childNum;
            myTree->setParent(childNum, nodeNum);
        }
    }
    char option; // to read in the option
    // read in the options and switch based on the option
    while (!cin.eof())
    {
        while (cin >> option)
        {
            //show solution
            if (option == 'D') {
                cout << "Parent Array of tree:" << endl;
                cout << *myTree;
            }
            //call root method
            if (option == 'O') {
                cout << "Root of tree: " << myTree->root() << endl;
            }
            //call height method
            if (option == 'H') {
                cout << "Height of tree: " << myTree->height() << endl;
            }
            //call parent method
            if (option == 'P') {
                cin >> nodeNum;
                cout << "Parent of " << nodeNum << ": " << myTree->parent(nodeNum) << endl;
            }
            //call children method
            if (option == 'C') {
                cin >> nodeNum;
                cout << "Children of " << nodeNum << ": " << endl;
                myTree->children(nodeNum);
            }
            //call sibling method
            if (option == 'S') {
                cin >> nodeNum;
                cout << "Siblings of " << nodeNum << ": " << endl;
                myTree->siblings(nodeNum);
            }
            //call level method
            if (option == 'L') {
                cin >> nodeNum;
                cout << "Level of " << nodeNum << ": " << myTree->level(nodeNum) << endl;
            }
            //call nodesAtLevel method
            if (option == 'N') {
                cin >> nodeNum;
                myTree->nodesAtLevel(nodeNum);
            }
            //call LCA method
            if (option == 'A') {
                cin >> nodeNum;
                cin >> childNum;
                cout << "LCA of " << nodeNum << " and " << childNum << ": " << myTree->LCA(nodeNum, childNum) << endl;
            }
            //call preorder method
            if (option == 'R') {
                cout << "Preorder traversal of tree:" << endl;
                myTree->preorder(-1);
            }
        }
    }

    return 0;
}