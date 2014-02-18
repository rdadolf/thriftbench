#include "Null.h" 

#include <transport/TSocket.h>
#include <transport/TBufferTransports.h>
#include <protocol/TBinaryProtocol.h>

using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

int main(int argc, char **argv) {
    boost::shared_ptr<TSocket> socket(new TSocket("localhost", 38003));
    boost::shared_ptr<TTransport> transport(new TFramedTransport(socket));
    boost::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));

    NullClient client(protocol);
    transport->open();
    int32_t i = 0; 
    for (; i < 100000; ++i) {
        client.identity(i);
    }
    printf("%d", i);
    transport->close();

    return 0;
}
