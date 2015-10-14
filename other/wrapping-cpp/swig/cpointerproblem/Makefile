all:
	swig -python example1.i
	gcc -fPIC -Wall -Wextra -I/usr/include/python2.7 -std=gnu99 -shared -o _example1.so example1_wrap.c

clean:
	rm *.so
	rm example*_wrap.c
	rm example*.py
	rm *.pyc

alternate:
	swig -python example2.i
	gcc -fPIC -Wall -Wextra -I/usr/include/python2.7 -std=gnu99 -shared -o _example2.so example2_wrap.c

