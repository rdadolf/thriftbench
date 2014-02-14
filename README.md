## Thrift Bench

A collection of simple performance metrics for Apache Thrift.

Benchmarks:

  - NULL RPC latency
  - Goodput vs. message size
  - Goodput vs. multiple clients/servers
  - Goodput vs. RPC window
  - Paxos throughput


## Running Python Tests

Go to the benchmark you want to in the `benchmarks` directory. The python files will be in the `py` directory.
You can run `make test` to see the test run. You can run `make` to recompile the thrift definitions, if you 
have changed them. 

Example:

        $ cd benchmarks/null
        $ make test
        thrift --out py --gen py null.thrift
        ./run_py.sh
        Listening on 38003
        3
        $

