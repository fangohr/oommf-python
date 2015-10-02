/* from http://www.swig.org/Doc3.0/Introduction.html#Introduction_nn8 

File : example.i */
%module example
%{
/* Put headers and other declarations here */
    extern double My_variable;
    extern int    fact(int);
    extern int    my_mod(int n, int m);
    extern char *get_time(); 
%}

extern double My_variable;
extern int    fact(int);
extern int    my_mod(int n, int m);
extern char *get_time();
