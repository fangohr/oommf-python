%module test2

%{
#include "test.h"
%}

%pythoncallback;
double f(double);
%nopythoncallback;

%ignore f;
%include "test.h"
