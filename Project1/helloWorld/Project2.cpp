// Project 2
// Fall 2021
// DSA 5005 Computing Structures
// Boiler Plate Code for Project 2
#include<iostream>
using namespace std;
//________________________________________Sparse Row Class________________________________________________________
class SparseRow 
{
protected:
	int row; // Row#
	int col; // Column#
	int value; // We will assume that all our values will be integers
	// you are restricted to add or modify the fields in the class
public:SparseRow (); // default constructor; row=-1;col=-1;value=0 
	  SparseRow(int r, int c, int v); // non default constructor
	  virtual ~SparseRow(); // Destructor
	  void display(); // print Row#, Column#, value
	  void setRow (int r); // setters
	  void setCol (int c);
	  void setValue (int v);
	  int getRow (); // getters
	  int getCol ();
	  int getValue ();
	  // other methods as you deem fit
};
SparseRow::SparseRow()
{
	row = -1;
	col = -1;
	value = 0;
}
SparseRow::SparseRow(int r, int c, int v)
{
	row = r;
	col = c;
	value = v;
}
SparseRow::display() {
	cout << row << col << value << endl;
}
SparseRow::setRow(int r) {
	row = r;
}
SparseRow::setCol(int c) {
	col = c;
}
SparseRow::setValue(int v) {
	value = v;
}
SparseRow::getRow(){
	return row; }
SparseRow::getCol() {
	return col;
}
SparseRow::getValue() {
	return Value;
}

//___________________________________________Matrix Class_____________________________________________________
class matrixClass
{
protected: 
	int numRows; // number of rows 
	int numCols; // number of columns
	int numNonZero; // number of non zero elements
	int commonValue; // read from input - assume 0
	SparseRow* mat; // an array of SparseRow objects of length numNonZero
		// you are restricted to add or modify the fields in the class
public: 
	matrixClass(); // default constructor
	matrixClass(int r, int c, int numNonZero); // non default constructor        
	~matrixClass(); // destructor        
	matrixClass(matrixClass& copyThis); // copy constructor
	void display(); // display in sparse row format
	void displayMatrix (); // display in matrix format
	void setValue(int pos, int i, int j, int val); // to set the value at location i, j; pos is to keep track of the position in mat
	int getValue(int i, int j); // return val at i, j
	int getNumRows(); // getter for numRows
	int getNumCols(); // getter for numCols
	int getValWithRowandCol(int row, int col); // given row and col number,return the value at that spot
	matrixClass* multiply(matrixClass* multiplier); // multiply method        
	matrixClass* add(matrixClass* addend); // add method        
	// BONUS: 
	matrixClass* transpose(); // transopse method        
	// TODO: Write the overloaded ostream operator - same as displayMatrix() method        
	// other methods as you deem fit
 };
matrixClass::matrixClass(int r, int c, int z); {
	numRows = r;
	numCols = c;
	numNonZero = z;
	commonValue = 0;
	SparseRow sparseRows[z];
	mat = sparseRows;
}
// main function
int main()
{
	int numRows, numCols, numNonZero;// read in all the numRows, numCols and numNonZero values from redirected input for matrix A
	cin >> numRows >> numCols >> numNonZero;// declare object for matrix A
	// read in the values and use setValue to set the values read in for A
	// display matrix A
	cout << "A in SparseRow format: " << endl;
	cout << "A in Matrix format: " << endl;    
	cout << A; // use ostream operator
	// read in all the numRows, numCols and numNonZero values from redirected input for matrix B
	cin >> numRows >> numCols >> numNonZero;
	// declare object for matrix B
	// read in the values and use setValue to set the values read in for B
	// display matrix B
	cout << "B in SparseRow format: " << endl;
	cout << "B in Matrix format: " << endl;     
	cout << B; // use ostream operator 
	// declare resultant matrix to store A * B
	// display resultant matrix
	cout << "RESULT A*B in SparseRow format: " << endl;
	cout << "RESULT A*B in Matrix format: " << endl;    
	cout << resultMultiply; // use ostream operator method
	// declare resultant matrix to store A + B
	// display resultant matrix
	cout << "RESULT A+B in SparseRow format: " << endl;
	cout << "RESULT A+B in Matrix format: " << endl;    
	cout << resultAdd;// use ostream operator method
	// BONUS
	// declare resultant matrix to store transpose of A
	// display resultant matrix
	// BONUS cout << "RESULT A^T in SparseRow format: " << endl;
	// BONUS cout << "RESULT A^T in Matrix format: " << endl;    
	// cout << resultTranspose; use ostream operator method
	return 0; 
}