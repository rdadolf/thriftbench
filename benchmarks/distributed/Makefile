all: protocol cpp

protocol: .protocol.generated

.protocol.generated: distributed.thrift
    thrift --out py --gen py null.thrift
    touch .protocol.generated

clean:
    rm -rf py/protocol
    rm -rf .protocol.generated

