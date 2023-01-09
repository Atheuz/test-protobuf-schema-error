# Get started
1. Create a virtualenv: `virtualenv .venv --python=3.10`
2. Activate the virtualenv: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run pytest: `pytest`
5. See that when `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=upb`, `pytest` fails to run.
6. Change `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=upb` to `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` in `pytest.ini`.
7. Run pytest `pytest`
8. See that when `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`, `pytest` runs without issue.

Similarly, if you downgrade to `protobuf==3.20.3` and run the test using `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp` or `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python`, it also succeeds: Only `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=upb` which became available in 4.x fails.

# Description
What's happening is that we are going into `common/terms_pb2.py` and manually replacing `from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2` with `from google_test.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2`.
Note that we are not doing this replacement in `common/options_pb2.py`, having this conflict of 2 different imports is necessary for the error to appear: i.e. if we do the replacement in `common/options_pb2.py`, then the error disappears and everything works fine, but this is not what we're doing on our end, in that we only do the replacement in one file and not all files.

The `descriptor_pb2.py` file was generated using `buf` version 1.11.0 and `protoc` version 3.20.3 using the following commands:

```
cd build
buf generate --config=buf.yaml --template=buf.gen.yaml
cp google/protobuf/descriptor_pb2.py ../google_test/protobuf/descriptor_pb2.py
```

The reason our organization does this replacement in the `common/terms_pb2.py` file is related to the Confluent Kafka Schema Registry, where apparently if we don't do this replacement the schema doesn't match what we have in our Confluent Kafka Schema Registry.
