#include "Null.h"

#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using boost::shared_ptr;

class NullHandler : virtual public NullIf {
 public:
  NullHandler() {
    // Your initialization goes here
  }

  int32_t identity(const int32_t i) {
    // Your implementation goes here
    printf("identity\n");
  }

  void oneway_test(const int32_t i) {
    // Your implementation goes here
    printf("oneway_test\n");
  }

};

int main(int argc, char **argv) {
  int port = 38003;
  shared_ptr<NullHandler> handler(new NullHandler());
  shared_ptr<TProcessor> processor(new NullProcessor(handler));
  shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
  shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
  shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

  TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
  return 0;
}

