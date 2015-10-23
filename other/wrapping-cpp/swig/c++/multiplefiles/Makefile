all:
	swig -c++ -python shapes.i
	g++ -c -O2 -fPIC square.cpp 
	g++ -c -O2 -fPIC rectangle.cpp
	g++ -c -O2 -fPIC shapes_wrap.cxx -I/usr/include/python2.7
	g++ -shared square.o rectangle.o shapes_wrap.o -o _shapes.so

clean: 
	rm *.so
	rm *.o
	rm *.cxx
	rm shapes.py
	rm *.pyc
