namespace py protocol

service Null {

	i32 identity(1: i32 p);

    void a(1: string a);

	oneway void oneway_test(1: i32 p);

}
