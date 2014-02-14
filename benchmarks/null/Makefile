all: protocol

protocol: null.thrift
	thrift --out py --gen py null.thrift
	thrift --o cpp --gen cpp null.thrift

test-py: protocol
	./run_py.sh

clean:
	rm -rf py/protocol

