## Running tests

`pip2 install -r requirements.txt`

Run core tests (note some tests skipped at end) with:

`./run_tests.sh`

To run all tests. This may incur TED rate-limiting:

`PYTHONPATH=$PYTHONPATH:$PWD/testSupport EXCLUDE_RATE_LIMITED=false python2 -m "unittest" discover -s ./resources/lib/ -p "*_test.py"`

## Releasing

- Run unit tests
- Run manual tests (ad-hoc at the moment)
    - Redeploy plugin as zip
- Bump version number
- Add to `CHANGELOG.md`
- Update `<news>` in `addon.xml`
- Update readme
- Run `build.sh`
- Unzip dist into `repo-plugins/plugin.video.ted.talks`