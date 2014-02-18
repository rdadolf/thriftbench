BENCHMARK=paxos

# TODO
# CXXFLAGS
# LDFLAGS

################################################################################

all: python

.PHONY: protocol python cpp

protocol: $(BENCHMARK).thrift
	thrift --out py --gen py $(BENCHMARK).thrift
	thrift --out cpp --gen cpp $(BENCHMARK).thrift

python: py/server.py py/client.py protocol
	# Do nothing

cpp: cpp/client cpp/server

cpp/client: cpp/client.cpp protocol
	$(CXX) $(CXXFLAGS) cpp/client.cpp -o cpp/client $(LDFLAGS)

cpp/server: cpp/server.cpp protocol
	$(CXX) $(CXXFLAGS) cpp/server.cpp -o cpp/server $(LDFLAGS)
