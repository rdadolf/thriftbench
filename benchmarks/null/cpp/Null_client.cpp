#include "Null.h" 

#include <transport/TSocket.h>
#include <transport/TBufferTransports.h>
#include <protocol/TBinaryProtocol.h>

using namespace apache::thrift;
using namespace apache::thrift::protocol;
using namespace apache::thrift::transport;

#define WINDOW_SIZE 40

int main(int argc, char **argv) {
    boost::shared_ptr<TSocket> socket(new TSocket("localhost", 38003));
    boost::shared_ptr<TTransport> transport(new TFramedTransport(socket));
    boost::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));

    NullClient client(protocol);
    transport->open();
    int32_t i = 0; 
    int32_t w = 0;
    int32_t r = 0;
    while (i < 50000) {
        for (w = 0; w < WINDOW_SIZE; ++w) {
            client.send_identity(i + w);
        }
        for (w = 0; w < WINDOW_SIZE; ++w) {
            r = client.recv_identity();
            assert (r == (i + w));
        }
        i += WINDOW_SIZE;
    }

    // Big messages
    // std::string b = std::string(60000, 'a');
    // while (i < 30000) {
    //     client.a(b);
    //     i++;
    // }

    transport->close();

    return 0;
}
