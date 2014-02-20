## ThriftBench

A collection of simple performance metrics for Apache Thrift.

Benchmarks:

  - NULL RPC latency
  - Goodput vs. message size
  - Goodput vs. multiple clients/servers
  - Goodput vs. RPC window
  - Paxos throughput


## Running Microbenchmarks

Go to the benchmark you want to in the `benchmarks` directory. The python files will be in the `py` directory, the C++ ones in the `cpp` directory.
You can run `make` to recompile the thrift definitions, if you have changed them. 
You can run `make test-py` or make test-cpp to see the test run. 

Example:

    $ cd benchmarks/null
    $ make test-py
    thrift --out py --gen py null.thrift
    thrift --out cpp --gen cpp null.thrift
    ./run_py.sh
    Listening on 38003
    3

Caveat Emptor: Currently, this is only functioning properly for `null`. Yes, really. Sorry about that.


## Running Paxos

Go to the `benchmarks/paxos` directory. Run `run.py`. This is a simple script that fires off a bunch of accepter/learner servers and then runs the proposer client. Note that this script has a race condition baked into it. If the program fails, it's likely that you've triggered it. Re-run the script and hope *harder*. If it fails continuously, you can increase the sleep delay.
