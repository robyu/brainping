# Tests
python -m unittest

python -m unittest tests/test_mqttif.py  # by file

#
# for the following, you must first cd into ./tests
python -m unittest test_mqttif # by module

python -m unittest test_mqttif.TestMqttIf # by class

python -m unittest test_mqttif.TestMqttIf.test_pub_rcv  # by method




