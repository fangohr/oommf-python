%module example2

%{
#include "example.h"
%}

%pythoncallback;
double f(double);
%nopythoncallback;

%ignore f;
%include "example.h"
