#include "mylib.h"
#include <iostream>

void helloworld(void) {
	 std::cout << "Hello, world!" << std::endl;
}

double squared(double x) {
	return x * x;
}

double myfunction(double (*f)(double x), double y) {
	return f(y);
}
