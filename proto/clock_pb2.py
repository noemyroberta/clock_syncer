# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/clock.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11proto/clock.proto\x12\x05\x63lock\"\"\n\x0bSyncRequest\x12\x13\n\x0b\x63lient_time\x18\x01 \x01(\x03\"#\n\x0cSyncResponse\x12\x13\n\x0bserver_time\x18\x01 \x01(\x03\"\x10\n\x0eGetTimeRequest\"\x18\n\x08TimeInfo\x12\x0c\n\x04time\x18\x01 \x01(\x03\"#\n\x11UpdateTimeRequest\x12\x0e\n\x06offset\x18\x01 \x01(\x03\"\x14\n\x12UpdateTimeResponse2\xb8\x01\n\tClockSync\x12\x31\n\x04Sync\x12\x12.clock.SyncRequest\x1a\x13.clock.SyncResponse\"\x00\x12\x33\n\x07GetTime\x12\x15.clock.GetTimeRequest\x1a\x0f.clock.TimeInfo\"\x00\x12\x43\n\nUpdateTime\x12\x18.clock.UpdateTimeRequest\x1a\x19.clock.UpdateTimeResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.clock_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SYNCREQUEST']._serialized_start=28
  _globals['_SYNCREQUEST']._serialized_end=62
  _globals['_SYNCRESPONSE']._serialized_start=64
  _globals['_SYNCRESPONSE']._serialized_end=99
  _globals['_GETTIMEREQUEST']._serialized_start=101
  _globals['_GETTIMEREQUEST']._serialized_end=117
  _globals['_TIMEINFO']._serialized_start=119
  _globals['_TIMEINFO']._serialized_end=143
  _globals['_UPDATETIMEREQUEST']._serialized_start=145
  _globals['_UPDATETIMEREQUEST']._serialized_end=180
  _globals['_UPDATETIMERESPONSE']._serialized_start=182
  _globals['_UPDATETIMERESPONSE']._serialized_end=202
  _globals['_CLOCKSYNC']._serialized_start=205
  _globals['_CLOCKSYNC']._serialized_end=389
# @@protoc_insertion_point(module_scope)
