_example.so: example_wrap.o example.o

	ld -shared example.o example_wrap.o -lpython2.7 -o _example.so 
	# attempt to make this work for OSX 10
	## http://www.expobrain.net/2011/01/23/swig-tutorial-for-mac-os-x/
	# ld -bundle -flat_namespace -undefined suppress -o _example.so example.o example_wrap.o

example_wrap.c: example.i example.c
	swig -python example.i


example_wrap.o: example_wrap.c
	gcc -c -fpic example.c example_wrap.c -I /usr/include/python2.7
	## Attempt to make this work on OSX 10.4 (didn't succeed)
	# gcc -c -arch i486 -fPIC example_wrap.c -I ~/anaconda3/include/python3.4m -o example_wrap.o 


# following http://www.expobrain.net/2011/01/23/swig-tutorial-for-mac-os-x/
example.o: example.c
	gcc -c -arch i486 -fPIC example.c -o example.o


clean:
	rm example.o example_wrap.c example_wrap.o _example.so example.py

test:
	make clean
	make _example.so
	py.test -v 