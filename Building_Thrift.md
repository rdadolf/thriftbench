## Notes on Building Thrift

Most of the Thrift documentation assumes that you have root access and can install packages directly with, say, `yum`. Instead, if you want to install locally, source is the best bet. Here's how.

### Install Boost

        $ ./bootstrap --prefix=BOOST_PREFIX
        $ ./b2 install

### Install Thrift

Thrift's `PY_PREFIX` environment variable is ignored in favor of using the python installation conventions. To install thrift libraries in a custom location, edit your `.pydistutils.cfg` file to set a local installation path for python libraries. For instance:

        [install]
        install-path = PYTHON_PREFIX

Now run:

        $ ./configure --prefix=THRIFT_PREFIX --with-boost=BOOST_PREFIX
        $ make
        $ make install
