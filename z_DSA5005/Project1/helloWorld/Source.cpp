#include <iostream>
using namespace std;


/**************************************** Matrix Class **************************************************/
class Matrix
{
public:
	int numRows;
	int numCols;
	int nonZeroVals;
	int** arr;
	int* sparseRows;
	Matrix(int, int, int);
	~Matrix();
	void make_arr();
	void print_arr();
	void print_sparse_rows();
	void display();
};
Matrix::Matrix(int a, int b, int c)
{
	//cout << "making " << a << "x" << b << " matrix. It has " << c << " non-zero elements." << endl;
	numRows = a;
	numCols = b;
	nonZeroVals = c;
	arr = new int* [numRows];
	sparseRows = new int[nonZeroVals * 3];
	for (int i = 0; i < numRows; i++) {
		arr[i] = new int[numCols]();
	}
}
void Matrix::display()
{
	cout << "Your matrix has " << numRows << " rows and " << numCols << " cols." << endl;
}
void Matrix::make_arr()
{	
	int k,pickRow,pickCol,valIn;
	for (k=0; k<nonZeroVals; k++)
	{
		cin >> pickRow >> pickCol >> valIn;
		arr[pickRow][pickCol] = valIn;
		sparseRows[k * 3] = pickRow;
		sparseRows[(k * 3) + 1] = pickCol;
		sparseRows[(k * 3) + 2] = valIn;
		//cout << "Position: " << pickRow << ',' << pickCol << " set to " << valIn << endl;
	}
}
void Matrix::print_arr()
{
	int i,j;
	cout << "Matrix Format" << endl;
	for (i=0;i<numRows;i++)
	{
		for (j = 0; j < numCols; j++) {
			cout << arr[i][j] << " ";
		}
		cout << endl;
	}
}
void Matrix::print_sparse_rows()
{
	int i;
	cout << "Sparse Rows: " << endl;
	cout << "Row | Col | Value" << endl;
	for (i = 0; i < nonZeroVals * 3; i++) {
		//Print new line for each sparse row
		if (i % 3 == 0 && i != 0) {
			cout << endl;
		}
		cout << sparseRows[i] << ' ';	
	}
	cout << endl;
}
Matrix::~Matrix()
{	/*
	for (int i = 0; i < numRows; i++) {
		delete[] arr[i];
	}
	delete[] arr;*/
	//cout << "destruct matrix" << endl;
}
/******************************************************************************************************/
void multiply_matrices(Matrix a, Matrix b)
{
	//Get data
	int aRows, bRows, bCols, arrSize, nonZeros, sum;
	aRows = a.numRows;
	bRows = b.numRows;
	bCols = b.numCols;
	nonZeros= 0;
	sum = 0;
	arrSize = aRows * bCols;
	try {
		//multiply
		for (int currentRow = 0; currentRow < aRows; currentRow++) {
			for (int currentCol = 0; currentCol < bCols; currentCol++) {
				for (int i = 0; i < bRows; i++) {
					sum += a.arr[currentRow][i] * b.arr[i][currentCol];
				}
				cout << sum << " ";
				sum = 0;
			}
			cout << endl;
		}
		if (a.numCols != b.numRows) {
			throw 1;
		}
	}
	catch (int e) {
		cout << "Matrix Dimension Mismatch for Addition exception thrown" << endl;
	}
}
int main() {
	int numRows, numCols, numNonZero, a, b, c;
	cout << "Matrix 1:" << endl;
	cin >> numRows >> numCols >> numNonZero;
	Matrix mat1 (numRows, numCols, numNonZero);
	mat1.make_arr();
	cout << "A:" << endl;
	mat1.print_sparse_rows();
	mat1.print_arr();
	cout << "Matrix 2:" << endl;
	cin >> a >> b >> c;
	Matrix mat2(a, b, c);
	mat2.make_arr();
	cout << "B:" << endl;
	mat2.print_sparse_rows();
	mat2.print_arr();
	cout << "RESULT:" << endl;
	multiply_matrices(mat1, mat2);
	cout << "DONE" << endl;
	return 0;
}