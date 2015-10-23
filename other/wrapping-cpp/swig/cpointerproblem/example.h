/* This example is taken from here - demonstrates problem with Python treating everything as an object */

double f(double x) {
  return x*x;
}

double myfun(double (*f)(double x), double y) {
  fprintf(stdout, "%g\n", f(2.0));
  return f(y);
}

typedef double (*fptr_t)(double);
fptr_t make_fptr() {
  return f;
}