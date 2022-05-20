// Project 2
// Fall 2021
// DSA 5005 Computing Structures
// Boiler Plate Code for Project 2
#include <iostream>
using namespace std;
//________________________________________Sparse Row Class________________________________________________________
class SparseRow
{
protected:
	int row; // Row#
	int col; // Column#
	int value; // We will assume that all our values will be integers
	// you are restricted to add or modify the fields in the class
public:
	SparseRow(); // default constructor; row=-1;col=-1;value=0 
	SparseRow(int r, int c, int v); // non default constructor
	//virtual ~SparseRow(); // Destructor
	void display(); // print Row#, Column#, value
	void setRow(int r); // setters
	void setCol(int c);
	void setValue(int v);
	int getRow(); // getters
	int getCol();
	int getValue();
};
SparseRow::SparseRow()
{
	//default constructor
	row = -1;
	col = -1;
	value = 0;
}
SparseRow::SparseRow(int r, int c, int v)
{
	//non-default constructor
	row = r;
	col = c;
	value = v;
}
void SparseRow::display() {
	//display SparseRow
	cout << row << ' ' << col << ' ' << value << endl;
}
void SparseRow::setRow(int r) {
	row = r; //set row
}
void SparseRow::setCol(int c) {
	col = c; //set column
}
void SparseRow::setValue(int v) {
	value = v; //set value
}
int SparseRow::getRow() {
	return row; //return row
}
int SparseRow::getCol() {
	return col; //return column
}
int SparseRow::getValue() {
	return value; //return value
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
	void displayMatrix(); // display in matrix format
	void setValue(int pos, int i, int j, int val); // to set the value at location i, j; pos is to keep track of the position in mat
	int getValue(int i, int j); // return val at i, j
	int getNumRows(); // getter for numRows
	int getNumCols(); // getter for numCols
	int getValWithRowandCol(int row, int col); // given row and col number,return the value at that spot
	matrixClass* multiply(matrixClass* multiplier); // multiply method
	matrixClass* add(matrixClass* addend); // add method
	matrixClass* transpose(); //transpose method
	friend ostream& operator<<(ostream& os, matrixClass& m);
	// BONUS: 
	//matrixClass* transpose(); // transopse method        
	// TODO: Write the overloaded ostream operator - same as displayMatrix() method        
	// other methods as you deem fit
};
matrixClass::matrixClass() {
	//default constructor
	numRows = 0;
	numCols = 0;
	numNonZero = 0;
	commonValue = 0;
	mat = new SparseRow[0];
}
matrixClass::matrixClass(int r, int c, int z){
	//constructor
	numRows = r;
	numCols = c;
	numNonZero = z;
	commonValue = 0;
	mat = new SparseRow[z];
}
matrixClass::matrixClass(matrixClass& copyThis) {
	//copy matrix
	numRows = copyThis.numRows;
	numCols = copyThis.numCols;
	numNonZero = copyThis.numNonZero;
	commonValue = copyThis.commonValue;
	//deep copy sparse row pointer
	mat = new SparseRow[copyThis.numNonZero];
	for (int i = 0; i < copyThis.numNonZero; i++) {
		mat[i] = copyThis.mat[i];
	}
}
matrixClass::~matrixClass() {
	delete[] mat; //destructor
}
void matrixClass::display() {
	//print sparse rows in order
	for (int i = 0; i < numCols; i++) {
		for (int j = 0; j < numRows; j++) {
			for (int k = 0; k < numNonZero; k++) {
				if (mat[k].getCol() == i && mat[k].getRow() == j) {
					mat[k].display();
				}
			}
		}
	}
}
void matrixClass::displayMatrix() {
	bool valFound = false;
	//iterate through each position
	for (int r = 0; r < numRows; r++) {
		for (int c = 0; c < numCols; c++) {
			valFound = false;
			//check sparse rows for value
			for (int i = 0; i < numNonZero; i++) {
				if (mat[i].getRow() == r && mat[i].getCol() == c) {
					cout << mat[i].getValue(); //if value found, cout value
					valFound = true;
					break;
				}
			}
			//if no value found cout common value
			if (!valFound) {
				cout << commonValue;
			}
			cout << ' ';
		}
		cout << endl;
	}
}
void matrixClass::setValue(int pos, int i, int j, int val){
	mat[pos].setRow(i); //set row
	mat[pos].setCol(j); //set col
	mat[pos].setValue(val); //set val
}
int matrixClass::getValue(int i, int j) {
	//if pos in sparse row return value
	for (int k = 0; k < numNonZero; k++) {
		if (mat[k].getRow() == i && mat[k].getCol() == j) {
			return mat[k].getValue();
		}
	}
	//if pos not in sparse row return common value
	return commonValue;
}
int matrixClass::getNumRows() {
	return numRows; //return # rows
}
int matrixClass::getNumCols() {
	return numCols; // return # cols
}
int matrixClass::getValWithRowandCol(int row, int col) {
	// if pos in sparse row return value
	for (int k = 0; k < numNonZero; k++) {
		if (mat[k].getRow() == row && mat[k].getCol() == col) {
			return mat[k].getValue();
		}
	}
	// if pos not in sparse row return common value
	return commonValue;
}
matrixClass* matrixClass::multiply(matrixClass* multiplier) {
	int sum, nonZeroCounter;
	sum = 0;
	nonZeroCounter = 0;
	//Create new matrix in memory
	matrixClass* matC = new matrixClass (numRows, multiplier->getNumCols(), numRows*multiplier->getNumCols());
	//Do multiplication and set values
	nonZeroCounter = 0;
	for (int currentRow = 0; currentRow < numRows; currentRow++) {
		for (int currentCol = 0; currentCol < multiplier->getNumCols(); currentCol++) {
			for (int i = 0; i < numCols; i++) {
				sum += this->getValue(currentRow, i) * multiplier->getValue(i, currentCol);
			}
			if (sum != 0) {
				matC->setValue(nonZeroCounter, currentRow, currentCol, sum);
				nonZeroCounter += 1;
			}
			sum = 0;
		}
	}
	//Set numNonZero of new Matrix
	matC->numNonZero = nonZeroCounter;
	//Create new arr of Sparse rows for new Matrix
	SparseRow* newMat = new SparseRow[nonZeroCounter];
	for (int i = 0; i < nonZeroCounter; i++) {
		newMat[i].setRow(matC->mat[i].getRow());
		newMat[i].setCol(matC->mat[i].getCol());
		newMat[i].setValue(matC->mat[i].getValue());
	}
	//Delete old Sparse row arr and set to new
	delete[] matC->mat;
	matC->mat = newMat;
	//Return Pointer to created Matrix
	return matC;
}
matrixClass* matrixClass::add(matrixClass* addend) {
	int tempVal;
	int nonZeroCounter = 0;
	int sum = 0;
	//Create new Matrix in memory
	matrixClass* matD = new matrixClass(numRows, numCols, numRows * numCols);
	//set sparse rows of new Matrix to matrix A
	for (int k = 0; k < numNonZero; k++) {
		matD->mat[k].setRow(mat[k].getRow());
		matD->mat[k].setCol(mat[k].getCol());
		matD->mat[k].setValue(mat[k].getValue());
		nonZeroCounter++;
	}
	//for sparse rows in matrix B, if pos match add value, else append sparse row
	for (int k = 0; k < addend->numNonZero; k++) {
		bool match_exist = false;
		for (int j = 0; j < numNonZero; j++) {
			//if match add values
			if (addend->mat[k].getRow() == matD->mat[j].getRow() && addend->mat[k].getCol() == matD->mat[j].getCol()) {
				tempVal = matD->mat[j].getValue();
				matD->mat[j].setValue(tempVal + addend->mat[k].getValue());
				match_exist = true;
			}
		}
		//if no match append sparse row
			if (!match_exist) {
			matD->mat[nonZeroCounter].setRow(addend->mat[k].getRow());
			matD->mat[nonZeroCounter].setCol(addend->mat[k].getCol());
			matD->mat[nonZeroCounter].setValue(addend->mat[k].getValue());
			nonZeroCounter++;
			}
	}
	//Set numNonZero of new Matrix
	matD->numNonZero = nonZeroCounter;
	//Create new arr of Sparse rows for new Matrix
	SparseRow* temp = new SparseRow[nonZeroCounter];
	for (int i = 0; i < nonZeroCounter; i++) {
		temp[i].setRow(matD->mat[i].getRow());
		temp[i].setCol(matD->mat[i].getCol());
		temp[i].setValue(matD->mat[i].getValue());
	}
	//Delete old Sparse row arr and set to new
	delete[] matD->mat;
	matD->mat = temp;
	//Return Pointer to created Matrix
	return matD;
}
matrixClass* matrixClass::transpose(){
	int matchCount = 0;
	matrixClass* matE = new matrixClass(numCols, numRows, numNonZero);
	//get sparse rows in order
	for (int i = 0; i < numCols; i++) {
		for (int j = 0; j < numRows; j++) {
			for (int k = 0; k < numNonZero; k++) {
				if (mat[k].getCol() == i && mat[k].getRow() == j) {
					matE->mat[matchCount] = SparseRow(i, j, mat[k].getValue());
					matchCount++;
				}
			}
		}
	}
	return matE;
}
//___________________________________________ostream operator____________________________________________________
ostream& operator<<(ostream& os, matrixClass& m) {
	for (int i = 0; i < m.getNumRows(); i++) {
		for (int j = 0; j < m.getNumCols(); j++) {
			os << m.getValue(i, j) << ' ';
		}
		os << endl;
	}
	return os;
}
//______________________________________________main function____________________________________________________
int main()
{
	int numRows, numCols, numNonZero, i, j, val;
	bool mult_err, add_err;
	mult_err = add_err = false; //err booleans
	// read in all the numRows, numCols and numNonZero values from redirected input for matrix A
	cin >> numRows >> numCols >> numNonZero;
	// declare object for matrix A
	matrixClass A(numRows, numCols, numNonZero);
	// read in the values and use setValue to set the values read in for A
	for (int k = 0; k < numNonZero; k++) {
		cin >> i >> j >> val;
		try {
			if (i < 0 || i > numRows) throw 1;
			if (j < 0 || j > numCols) throw 2;
		}
		catch(int e){
			if (e == 1) cout << "Row Out of Bounce exception thrown - stopping execution" << endl;
			if (e == 2) cout << "Column Out of Bounce exception thrown - stopping execution" << endl;
			return 0;
		}
		A.setValue(k, i, j, val);
	}
	// display matrix A
	cout << "A in SparseRow format: " << endl;
	cout << "Row | Col | Value" << endl;
	A.display();
	cout << "A in Matrix format: " << endl;
	cout << A; // use ostream operator
	// read in all the numRows, numCols and numNonZero values from redirected input for matrix B
	cin >> numRows >> numCols >> numNonZero;
	// declare object for matrix B
	matrixClass B(numRows, numCols, numNonZero);
	// read in the values and use setValue to set the values read in for B
	for (int k = 0; k < numNonZero; k++) {
		cin >> i >> j >> val;
		try {
			if (i < 0 || i > numRows) throw 1;
			if (j < 0 || j > numCols) throw 2;
		}
		catch (int e) {
			if (e == 1) cout << "Row Out of Bounce exception thrown - stopping execution" << endl;
			if (e == 2) cout << "Column Out of Bounce exception thrown - stopping execution" << endl;
			return 0;
		}
		B.setValue(k, i, j, val);
	}
	// display matrix B
	cout << "B in SparseRow format: " << endl;
	cout << "Row | Col | Value" << endl;
	B.display();
	cout << "B in Matrix format: " << endl;
	cout << B; // use ostream operator 
	// declare resultant matrix to store A * B
	try {
		if (A.getNumCols() != B.getNumRows()) throw 3; //check dim for multiplication
	}
	catch (int e) {
		if (e == 3) {
			cout << "Matrix Dimension Mismatch for Multiplication exception thrown" << endl;
			mult_err = true;
		}
	}
	//if no multiplication error, do multiplication
	if (!mult_err) {
		matrixClass* C = new matrixClass(*A.multiply(&B));
		// display resultant matrix
		cout << "RESULT A*B in SparseRow format:" << endl;
		cout << "Row | Col | Value" << endl;
		C->display();
		cout << "RESULT A*B in Matrix format: " << endl;
		//C->displayMatrix();
		cout << *C; // use ostream operator method
		delete C;
	}
	try {
		if (A.getNumCols() != B.getNumCols() || A.getNumRows() != B.getNumRows()) throw 4; //check dim for addition
	}
	catch (int e) {
		if (e == 4) {
			cout << "Matrix Dimension Mismatch for Addition exception thrown" << endl;
			add_err = true; //addition error
		}
	}
	//if no addition error, do addition
	if (!add_err) {
		// declare resultant matrix to store A + B
		matrixClass* D = new matrixClass(*A.add(&B));
		// display resultant matrix
		cout << "Result A+B SparseRow format:" << endl;
		cout << "Row | Col | Value" << endl;
		D->display();
		cout << "Result A+B Matrix format:" << endl;
		cout << *D;// use ostream operator method
		delete D;
	}
	// BONUS
	// declare resultant matrix to store transpose of A
	//matrixClass* E = new matrixClass(*A.transpose());
	// display resultant matrix
	//cout << "RESULT A^T in SparseRow format:" << endl;
	//cout << "Row | Col | Value" << endl;
	//E->display();
	//cout << "RESULT A^T in Matrix format:" << endl;
	//cout << *E;
	//delete E;
	return 0;
}