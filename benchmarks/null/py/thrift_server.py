

class Handler:
    def identity(i):
        return i

    def oneway_test(i):
        pass

processor = OperationService.Processor(self)
transport = TSocket.TServerSocket(port=self.port)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
# the choice of this implementation is important!
server = TServer.TThreadedServer(processor, transport, tfactory, pfactory, daemon=True)


if __name__ == '__main__':
    try:
        server.serve()
    except KeyboardInterrupt:
        pass
