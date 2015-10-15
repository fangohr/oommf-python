%module mylib

// Make mylib_wrap.cxx include this header:
%{
#include "mylib.h"
%}

%pythoncallback;
double squared(double);
%nopythoncallback;


// Make SWIG look into this header:
%ignore squared;
%include "mylib.h"
