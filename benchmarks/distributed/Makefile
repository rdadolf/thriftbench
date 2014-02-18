all: protocol

protocol: .protocol.generated

.protocol.generated: distributed.thrift
	thrift --out py --gen py distributed.thrift
	touch .protocol.generated

clean:
	rm -rf py/protocol
	rm -rf .protocol.generated

