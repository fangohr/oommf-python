all:
	swig -python test.i
	gcc -fPIC -Wall -Wextra -I/usr/include/python2.7 -std=gnu99 -shared -o _test.so test_wrap.c

clean:
	rm *.so
	rm test_wrap.c
	rm test.py
	rm *.pyc

alternate:
	swig -python test2.i
	gcc -fPIC -Wall -Wextra -I/usr/include/python2.7 -std=gnu99 -shared -o _test2.so test2_wrap.c

