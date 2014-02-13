## Notes on Building Thrift

Thrift assumes that you have root access when building from source.

### Install Boost

        $ ./bootstrap --prefix=BOOST_PREFIX
        $ ./b2 install

### Install Thrift

Edit your .pydistutils.cfg file to set a local installation path for python libraries. For instance:

        [install]
        install-path = PYTHON_PREFIX

Now run:

        $ ./configure --prefix=THRIFT_PREFIX --with-boost=BOOST_PREFIX
        $ make
        $ make install
