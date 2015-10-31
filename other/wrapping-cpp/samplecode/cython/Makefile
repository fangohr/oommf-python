rect.so:
	python setup.py build_ext --inplace

clean:
	rm -f rect.so rect.cpp

test:
	make clean
	make build_
	py.test -v 


.PHONY: clean test
