all: protocol cpp

protocol: .protocol.generated

.protocol.generated: null.thrift
	thrift --out py --gen py null.thrift
	thrift --out cpp --gen cpp null.thrift
	touch .protocol.generated

test-py: protocol
	./run_py.sh

test-cpp: cpp
	./run_cpp.sh

cpp: protocol
	cd cpp; make

clean:
	rm -rf py/protocol
	rm -rf .protocol.generated
	cd cpp; make clean

