#include <iostream>
using namespace std;

//------------------------------Point Class-------------------------------------
class Point
{
private:
  double _x;
  double _y;
public:
  Point();
  Point(double x, double y);
  void setX (double x);
  void setY (double y);
  double getX();
  double getY();
  void display();
};

Point::Point()
{
  _x = 0;
  _y = 0;
}

Point::Point(double x, double y)
{
  _x = x;
  _y = y;
}

void Point::setX(double x)
{
  _x = x;
}

void Point::setY(double y)
{
  _y = y;
}

double Point::getX()
{
  return _x;
}

double Point::getY()
{
  return _y;
}

void Point::display()
{
  cout << "x = " << _x << " y = " << _y << endl;
}
//------------------------------------------------------------------------------

int main()
{
  Point p1; //point with no constructors
  Point p2(5,10); //point with constructors
  p1.display();
  p2.display();

  return 0;
}
