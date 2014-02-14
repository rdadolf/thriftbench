all: protocol

protocol: null.thrift
	thrift --out py --gen py null.thrift

clean:
	rm -rf py/protocol

