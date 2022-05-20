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
	Matrix(int, int, int);
	~Matrix();
	void make_arr();
	void print_arr();
};
Matrix::Matrix(int a, int b, int c)
{
	numRows = a;
	numCols = b;
	nonZeroVals = c;
	arr = new int* [numRows];
	for (int i = 0; i < numRows; i++) {
		arr[i] = new int[numCols]();
	}
}
void Matrix::make_arr()
{
	int k, pickRow, pickCol, valIn;
	for (k = 0; k < nonZeroVals; k++)
	{
		cin >> pickRow >> pickCol >> valIn;
		arr[pickRow][pickCol] = valIn;
	}
}
void Matrix::print_arr()
{
	int i, j;
	for (i = 0; i < numRows; i++)
	{
		for (j = 0; j < numCols; j++) {
			cout << arr[i][j] << " ";
		}
		cout << endl;
	}
}
Matrix::~Matrix()
{
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
	nonZeros = 0;
	sum = 0;
	arrSize = aRows * bCols;
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
}
int main() {
	int numRows, numCols, numNonZero, a, b, c;
	//Create Matrix 1
	cin >> numRows >> numCols >> numNonZero;
	Matrix mat1(numRows, numCols, numNonZero);
	mat1.make_arr();

	//output Matrix 1
	cout << "A:" << endl;
	mat1.print_arr();

	//Create Matrix 2
	cin >> a >> b >> c;
	Matrix mat2(a, b, c);
	mat2.make_arr();

	//output Matrix 2
	cout << "B:" << endl;
	mat2.print_arr();

	//Multiply
	cout << "RESULT:" << endl;
	multiply_matrices(mat1, mat2);
	return 0;
}