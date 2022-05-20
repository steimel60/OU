#include <iostream>
#include <list>
#include <iterator>

using namespace std;

//-------------------------------------------- Set Array Class --------------------------------------------------
template <class DT>
class setArrayClass
{
protected:
    list<DT>* arrOfSets; // array of sets/lists
    int lengthOfArray; // length of the array / number of sets
public:
    setArrayClass(); // default constructor
    setArrayClass(int n); // non default constructor
    ~setArrayClass(); //destructor
    int getLength(); // get the number of sets / array length
    void setLength(int l); // set the length field with the l value
    list<DT> getSet(int i); // return A[i]
    void setValue(int setIndex, DT val); // set the value val in the setIndex position's set
    void display(); // display in the given format the array of sets
    list<DT> setIntersection(list<DT> l1, int l); // find the intersection between set l1and A[l] and return result
    list<DT> setUnion(list<DT> l1, int l);// find the union between set l1 and A[l] and return result
    list<DT> setCompliment(int l); // find the compliment of A[l] and return that list
    // other methods necessary
};
//------------ Methods ------------//
template <class DT>
setArrayClass<DT>::setArrayClass() {
    lengthOfArray = 0;
    arrOfSets = new list<DT> [1];
    lengthOfArray = 1;
}
template <class DT>
setArrayClass<DT>::setArrayClass(int n) {
    lengthOfArray = 0;
    arrOfSets = new list<DT> [n];
    lengthOfArray = n;
}
template <class DT>
setArrayClass<DT>::~setArrayClass() {
    delete[] arrOfSets;
}
template <class DT>
int setArrayClass<DT>::getLength() {
    return lengthOfArray;
}
template <class DT>
void setArrayClass<DT>::setLength(int l) {
    lengthOfArray = l;
}
template <class DT>
list<DT> setArrayClass<DT>::getSet(int i) {
    return arrOfSets[i];
}
template <class DT>
void setArrayClass<DT>::setValue(int setIndex, DT val) {
    arrOfSets[setIndex].push_back(val);
}
template <class DT>
void setArrayClass<DT>::display() {
    for (int i = 0; i < lengthOfArray; i++) {
        cout << "A[" << i << "]: ";
        //iterate and print value
        for (auto j = arrOfSets[i].begin(); j != arrOfSets[i].end(); j++) {
            cout << *j << " ";
        }
        cout << endl;
    }
}
template <class DT>
list<DT> setArrayClass<DT>::setCompliment(int l) {
    list<DT> result;
    bool in_set;
    //iterate through all possible numbers (for this project)
    for (int j = 0; j <= 20; j++) {
        in_set = false;
        //iterate through second list
        for (typename list<DT>::iterator i = arrOfSets[l].begin(); i != arrOfSets[l].end(); i++) {
            if (*i == j) {
                //if j in set change bool
                in_set = true;
                break;
            }
        }
        //If value not in set, add to compliment list
        if (!in_set) {
            result.push_back(j);
        }
    }
    return result;
}
template <class DT>
list<DT> setArrayClass<DT>::setIntersection(list<DT> l1, int l) {
    list<DT> result, temp;
    //check for compliment op
    if (l < 0) {
        temp = this->setCompliment(-l);
    }
    else {
        temp = arrOfSets[l];
    }
    //iterate through list
    for (typename list<DT>::iterator j = l1.begin(); j != l1.end(); j++) {
        //iterate through other list
        for (typename list<DT>::iterator i = temp.begin(); i != temp.end(); i++) {
            if (*i == *j) {
                //add match to list
                result.push_back(*i);
                break;
            }
        }
    }
    return result;
}
template <class DT>
list<DT> setArrayClass<DT>::setUnion(list<DT> l1, int l) {
    list<DT> result = l1;
    list<DT> temp;
    //check for compliment op
    if (l < 0) {
        temp = this->setCompliment(-l);
    }
    else {
        temp = arrOfSets[l];
    }
    bool in_set;
    //iterate through list
    for (typename list<DT>::iterator i = temp.begin(); i != temp.end(); i++) {
        in_set = false;
        for (typename list<DT>::iterator j = l1.begin(); j != l1.end(); j++) {
            if (*i == *j) {
                //if j in set change bool
                in_set = true;
                break;
            }
        }
        //if not in set 1 append it
        if (!in_set) {
            result.push_back(*i);
        }
    }
    return result;
}

//------------------------------------------------ Main Func -----------------------------------------------------------
int main()
{
    int numLists, numElements;
    char oper;
    int val1, val2;
    // read in the number of lists/array length and the number of total elements
    cin >> numLists >> numElements;
    // arr1 is the array of lists
    setArrayClass<int>* arr1 = new setArrayClass<int>(numLists);
    // read in the number pairs and insert the element to the specific set index
    for (int i = 0; i < numElements; i++)
    {
        cin >> val1 >> val2;
        if (val1 < numElements) {
            arr1->setValue(val1, val2);
        }
        else {
            i--;
        }
    }
    // display the array of sets
    cout << "Input array of sets: " << endl;
    arr1->display();
    // read all the expressions to evaluate them and display the answer
    list<int> temp_list;
    int exp_counter = 1;
    int op_counter = 0;
    while (!cin.eof())
    {
        // if first value in function get list from arr
        if (op_counter == 0) {
            cin >> val1;
            temp_list = arr1->getSet(val1);
            cout << endl;
        }
        while (cin >> oper)
        {
            //show solution
            if (oper == ';')
            {
                cout << "Expression " << exp_counter << ":" << endl;
                exp_counter++;
                for (auto j = temp_list.begin(); j != temp_list.end(); j++) {
                    cout << *j << " ";
                }
                op_counter = 0;
                break;
            }
            //call union method
            if (oper == '+') {
                cin >> val2;
                temp_list = arr1->setUnion(temp_list, val2);
            }
            //call intersection method
            if (oper == '*') {
                cin >> val2;
                temp_list = arr1->setIntersection(temp_list, val2);
            }
        }
    }
    return 0;
}