## Running tests

`pip3 install -r requirements.txt`

Run core tests (note some tests skipped at end) with:

`./run_tests.sh`

To run all tests. This may incur TED rate-limiting:

`EXCLUDE_RATE_LIMITED=false python2 -m "unittest" discover -s ./resources/lib/ -p "*_test.py"`

## Releasing

- Run unit tests
- Run manual tests (ad-hoc at the moment)
- Bump version number
- Add to `CHANGELOG.md`
- Update `<news>` in `addon.xml`
- Update readme
- Run `build.sh`
  - Install as zip
- Unzip dist into `repo-plugins/plugin.video.ted.talks`
