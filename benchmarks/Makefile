all_tests: ping


ping: ping.thrift ping_client.py ping_server.py
	thrift -gen py ping.thrift
	rm -r ping
	mv gen-py/ping .
	rm -r gen-py

