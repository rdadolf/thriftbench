namespace py paxos

// Datatype for tuples
struct prepare_t {
  1: i32 n
  2: i32 v
}

struct accept_t {
  1: i32 n
  2: i32 v
}

service Paxos {
  // Response functions
  prepare_t prepare(1:i32 n)
  i32 accept(1:accept_t nv)
  void decide(1:i32 v)
}
