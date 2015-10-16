#include "rectangle.h"

rectangle::rectangle(int x, int y){
	a = x;
	b = y;
}

int rectangle::area(void) {
	return a*b;
}
