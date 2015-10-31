test: build
	py.test -v

build:
	@echo "Compiling necessary files."
	make -C other/wrapping-cpp/swig/c/manual-example1/ all
	make -C other/wrapping-cpp/samplecode/cython/
