`pip2 install -r requirements.txt`

Run core tests (note some tests skipped at end) with:

`PYTHONPATH=$PYTHONPATH:$PWD/testSupport python2 -m "nose"`

To run all tests. This may incur TED rate-limiting:

`PYTHONPATH=$PYTHONPATH:$PWD/testSupport EXCLUDE_RATE_LIMITED=false python2 -m "nose"`
