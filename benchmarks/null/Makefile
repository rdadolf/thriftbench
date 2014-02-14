all: protocol

protocol: null.thrift
	thrift --out py --gen py null.thrift

test: protocol
	./run_py.sh

clean:
	rm -rf py/protocol

