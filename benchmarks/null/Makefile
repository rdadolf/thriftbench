all: protocol cpp

protocol: null.thrift
	thrift --out py --gen py null.thrift
	thrift --out cpp --gen cpp null.thrift

test-py: protocol
	./run_py.sh

test-cpp: cpp
	./run_cpp.sh

cpp: protocol
	cd cpp; make

clean:
	rm -rf py/protocol
	cd cpp; make clean

