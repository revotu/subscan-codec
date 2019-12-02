# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rpc.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rpc.proto',
  package='codec_protos',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\trpc.proto\x12\x0c\x63odec_protos\"<\n\x10\x45xtrinsicRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x17\n\x0fmetadataVersion\x18\x02 \x01(\x05\"0\n\x0e\x45xtrinsicReply\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\x08\"8\n\x0c\x45ventRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x17\n\x0fmetadataVersion\x18\x02 \x01(\x05\",\n\nEventReply\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\r\n\x05\x65rror\x18\x02 \x01(\x08\"6\n\nLogRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x17\n\x0fmetadataVersion\x18\x02 \x01(\x05\"\x1b\n\x08LogReply\x12\x0f\n\x07message\x18\x01 \x01(\t\"6\n\x0eStorageRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65\x63oderType\x18\x02 \x01(\t\"\x1f\n\x0cStorageReply\x12\x0f\n\x07message\x18\x01 \x01(\t\";\n\x0fMetadataRequest\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x17\n\x0fmetadataVersion\x18\x02 \x01(\x05\" \n\rMetadataReply\x12\x0f\n\x07message\x18\x01 \x01(\x08\x32\xfc\x02\n\x05Tools\x12Q\n\x0f\x44\x65\x63odeExtrinsic\x12\x1e.codec_protos.ExtrinsicRequest\x1a\x1c.codec_protos.ExtrinsicReply\"\x00\x12\x45\n\x0b\x44\x65\x63odeEvent\x12\x1a.codec_protos.EventRequest\x1a\x18.codec_protos.EventReply\"\x00\x12?\n\tDecodeLog\x12\x18.codec_protos.LogRequest\x1a\x16.codec_protos.LogReply\"\x00\x12K\n\rDecodeStorage\x12\x1c.codec_protos.StorageRequest\x1a\x1a.codec_protos.StorageReply\"\x00\x12K\n\x0bRegMetadata\x12\x1d.codec_protos.MetadataRequest\x1a\x1b.codec_protos.MetadataReply\"\x00\x62\x06proto3')
)




_EXTRINSICREQUEST = _descriptor.Descriptor(
  name='ExtrinsicRequest',
  full_name='codec_protos.ExtrinsicRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.ExtrinsicRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadataVersion', full_name='codec_protos.ExtrinsicRequest.metadataVersion', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=87,
)


_EXTRINSICREPLY = _descriptor.Descriptor(
  name='ExtrinsicReply',
  full_name='codec_protos.ExtrinsicReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.ExtrinsicReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='codec_protos.ExtrinsicReply.error', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=89,
  serialized_end=137,
)


_EVENTREQUEST = _descriptor.Descriptor(
  name='EventRequest',
  full_name='codec_protos.EventRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.EventRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadataVersion', full_name='codec_protos.EventRequest.metadataVersion', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=139,
  serialized_end=195,
)


_EVENTREPLY = _descriptor.Descriptor(
  name='EventReply',
  full_name='codec_protos.EventReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.EventReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='codec_protos.EventReply.error', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=197,
  serialized_end=241,
)


_LOGREQUEST = _descriptor.Descriptor(
  name='LogRequest',
  full_name='codec_protos.LogRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.LogRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadataVersion', full_name='codec_protos.LogRequest.metadataVersion', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=243,
  serialized_end=297,
)


_LOGREPLY = _descriptor.Descriptor(
  name='LogReply',
  full_name='codec_protos.LogReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.LogReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=299,
  serialized_end=326,
)


_STORAGEREQUEST = _descriptor.Descriptor(
  name='StorageRequest',
  full_name='codec_protos.StorageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.StorageRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='decoderType', full_name='codec_protos.StorageRequest.decoderType', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=328,
  serialized_end=382,
)


_STORAGEREPLY = _descriptor.Descriptor(
  name='StorageReply',
  full_name='codec_protos.StorageReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.StorageReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=384,
  serialized_end=415,
)


_METADATAREQUEST = _descriptor.Descriptor(
  name='MetadataRequest',
  full_name='codec_protos.MetadataRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.MetadataRequest.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadataVersion', full_name='codec_protos.MetadataRequest.metadataVersion', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=417,
  serialized_end=476,
)


_METADATAREPLY = _descriptor.Descriptor(
  name='MetadataReply',
  full_name='codec_protos.MetadataReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='codec_protos.MetadataReply.message', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=478,
  serialized_end=510,
)

DESCRIPTOR.message_types_by_name['ExtrinsicRequest'] = _EXTRINSICREQUEST
DESCRIPTOR.message_types_by_name['ExtrinsicReply'] = _EXTRINSICREPLY
DESCRIPTOR.message_types_by_name['EventRequest'] = _EVENTREQUEST
DESCRIPTOR.message_types_by_name['EventReply'] = _EVENTREPLY
DESCRIPTOR.message_types_by_name['LogRequest'] = _LOGREQUEST
DESCRIPTOR.message_types_by_name['LogReply'] = _LOGREPLY
DESCRIPTOR.message_types_by_name['StorageRequest'] = _STORAGEREQUEST
DESCRIPTOR.message_types_by_name['StorageReply'] = _STORAGEREPLY
DESCRIPTOR.message_types_by_name['MetadataRequest'] = _METADATAREQUEST
DESCRIPTOR.message_types_by_name['MetadataReply'] = _METADATAREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ExtrinsicRequest = _reflection.GeneratedProtocolMessageType('ExtrinsicRequest', (_message.Message,), dict(
  DESCRIPTOR = _EXTRINSICREQUEST,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.ExtrinsicRequest)
  ))
_sym_db.RegisterMessage(ExtrinsicRequest)

ExtrinsicReply = _reflection.GeneratedProtocolMessageType('ExtrinsicReply', (_message.Message,), dict(
  DESCRIPTOR = _EXTRINSICREPLY,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.ExtrinsicReply)
  ))
_sym_db.RegisterMessage(ExtrinsicReply)

EventRequest = _reflection.GeneratedProtocolMessageType('EventRequest', (_message.Message,), dict(
  DESCRIPTOR = _EVENTREQUEST,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.EventRequest)
  ))
_sym_db.RegisterMessage(EventRequest)

EventReply = _reflection.GeneratedProtocolMessageType('EventReply', (_message.Message,), dict(
  DESCRIPTOR = _EVENTREPLY,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.EventReply)
  ))
_sym_db.RegisterMessage(EventReply)

LogRequest = _reflection.GeneratedProtocolMessageType('LogRequest', (_message.Message,), dict(
  DESCRIPTOR = _LOGREQUEST,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.LogRequest)
  ))
_sym_db.RegisterMessage(LogRequest)

LogReply = _reflection.GeneratedProtocolMessageType('LogReply', (_message.Message,), dict(
  DESCRIPTOR = _LOGREPLY,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.LogReply)
  ))
_sym_db.RegisterMessage(LogReply)

StorageRequest = _reflection.GeneratedProtocolMessageType('StorageRequest', (_message.Message,), dict(
  DESCRIPTOR = _STORAGEREQUEST,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.StorageRequest)
  ))
_sym_db.RegisterMessage(StorageRequest)

StorageReply = _reflection.GeneratedProtocolMessageType('StorageReply', (_message.Message,), dict(
  DESCRIPTOR = _STORAGEREPLY,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.StorageReply)
  ))
_sym_db.RegisterMessage(StorageReply)

MetadataRequest = _reflection.GeneratedProtocolMessageType('MetadataRequest', (_message.Message,), dict(
  DESCRIPTOR = _METADATAREQUEST,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.MetadataRequest)
  ))
_sym_db.RegisterMessage(MetadataRequest)

MetadataReply = _reflection.GeneratedProtocolMessageType('MetadataReply', (_message.Message,), dict(
  DESCRIPTOR = _METADATAREPLY,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:codec_protos.MetadataReply)
  ))
_sym_db.RegisterMessage(MetadataReply)



_TOOLS = _descriptor.ServiceDescriptor(
  name='Tools',
  full_name='codec_protos.Tools',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=513,
  serialized_end=893,
  methods=[
  _descriptor.MethodDescriptor(
    name='DecodeExtrinsic',
    full_name='codec_protos.Tools.DecodeExtrinsic',
    index=0,
    containing_service=None,
    input_type=_EXTRINSICREQUEST,
    output_type=_EXTRINSICREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DecodeEvent',
    full_name='codec_protos.Tools.DecodeEvent',
    index=1,
    containing_service=None,
    input_type=_EVENTREQUEST,
    output_type=_EVENTREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DecodeLog',
    full_name='codec_protos.Tools.DecodeLog',
    index=2,
    containing_service=None,
    input_type=_LOGREQUEST,
    output_type=_LOGREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='DecodeStorage',
    full_name='codec_protos.Tools.DecodeStorage',
    index=3,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGEREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='RegMetadata',
    full_name='codec_protos.Tools.RegMetadata',
    index=4,
    containing_service=None,
    input_type=_METADATAREQUEST,
    output_type=_METADATAREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_TOOLS)

DESCRIPTOR.services_by_name['Tools'] = _TOOLS

# @@protoc_insertion_point(module_scope)
