all:
	swig -c++ -python mylib.i
	g++ -c -O2 -fPIC mylib.cc 
	g++ -c -O2 -fPIC mylib_wrap.cxx -I/usr/include/python2.7
	g++ -shared mylib.o mylib_wrap.o -o _mylib.so

clean: 
	rm -f *.so
	rm -f *.o
	rm -f *.cxx
	rm mylib.py
	rm -f *.pyc
