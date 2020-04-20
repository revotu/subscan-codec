# Python SCALE Codec Library
#
# Copyright 2018-2019 openAware BV (NL).
# This file is part of Polkascan.
#
# Polkascan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Polkascan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Polkascan. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from pkg.scalecodec.base import ScaleType, ScaleBytes


class Compact(ScaleType):

    def __init__(self, data, **kwargs):
        self.compact_length = 0
        self.compact_bytes = None
        super().__init__(data, **kwargs)

    def process_compact_bytes(self):
        compact_byte = self.get_next_bytes(1)
        if len(compact_byte) == 0:
            byte_mod = 0
        else:
            byte_mod = compact_byte[0] % 4
        if byte_mod == 0:
            self.compact_length = 1
        elif byte_mod == 1:
            self.compact_length = 2
        elif byte_mod == 2:
            self.compact_length = 4
        else:
            self.compact_length = int(5 + (compact_byte[0] - 3) / 4)

        if self.compact_length == 1:
            self.compact_bytes = compact_byte
        elif self.compact_length in [2, 4]:
            self.compact_bytes = compact_byte + self.get_next_bytes(self.compact_length - 1)
        else:
            self.compact_bytes = self.get_next_bytes(self.compact_length - 1)

        return self.compact_bytes

    def process(self):

        self.process_compact_bytes()

        if self.sub_type:

            byte_data = self.get_decoder_class(self.sub_type, ScaleBytes(self.compact_bytes)).process()

            # TODO Assumptions
            if (type(byte_data) is str and byte_data.isdigit() or type(byte_data) is int) and self.compact_length <= 4:
                return int(int(byte_data) / 4)
            else:
                # TODO raise exception?
                return byte_data
        else:
            return self.compact_bytes


# Example of specialized composite implementation for performance improvement
class CompactU32(Compact):
    type_string = 'Compact<u32>'

    def process(self):
        self.process_compact_bytes()

        if self.compact_length <= 4:
            return int(int.from_bytes(self.compact_bytes, byteorder='little') / 4)
        else:
            return int.from_bytes(self.compact_bytes, byteorder='little')

    def encode(self, value: int):

        if value <= 0b00111111:
            self.data = ScaleBytes(bytearray(int(value << 2).to_bytes(1, 'little')))

        elif value <= 0b0011111111111111:
            self.data = ScaleBytes(bytearray(int((value << 2) | 0b01).to_bytes(2, 'little')))

        elif value <= 0b00111111111111111111111111111111:

            self.data = ScaleBytes(bytearray(int((value << 2) | 0b10).to_bytes(4, 'little')))

        else:
            for bytes_length in range(4, 68):
                if 2 ** (8 * (bytes_length - 1)) <= value < 2 ** (8 * bytes_length):
                    self.data = ScaleBytes(bytearray(
                        ((bytes_length - 4) << 2 | 0b11).to_bytes(1, 'little') + value.to_bytes(bytes_length,
                                                                                                'little')))
                    break
            else:
                raise ValueError('{} out of range'.format(value))

        return self.data


class Option(ScaleType):
    def process(self):
        option_byte = self.get_next_bytes(1)

        if self.sub_type and option_byte != b'\x00':
            return self.process_type(self.sub_type).value

        return None

    def encode(self, value):

        if value is not None and self.sub_type:
            sub_type_obj = self.get_decoder_class(self.sub_type)
            return ScaleBytes('0x01') + sub_type_obj.encode(value)

        return ScaleBytes('0x00')


class Bytes(ScaleType):
    type_string = 'Vec<u8>'

    def process(self):

        length = self.process_type('Compact<u32>').value
        value = self.get_next_bytes(length)

        try:
            return value.decode()
        except UnicodeDecodeError:
            return value.hex()


class OptionBytes(ScaleType):
    type_string = 'Option<Vec<u8>>'

    def process(self):
        option_byte = self.get_next_bytes(1)

        if option_byte != b'\x00':
            return self.process_type('Bytes').value

        return None


# TODO replace in metadata
class String(ScaleType):

    def process(self):
        length = self.process_type('Compact<u32>').value
        value = self.get_next_bytes(length)

        return value.decode()


class HexBytes(ScaleType):

    def process(self):
        length = self.process_type('Compact<u32>').value

        return '0x{}'.format(self.get_next_bytes(length).hex())


class U8(ScaleType):

    def process(self):
        return self.get_next_u8()

    def encode(self, value):
        if 0 <= value <= 2 ** 8 - 1:
            self.data = ScaleBytes(bytearray(int(value).to_bytes(1, 'little')))
        else:
            raise ValueError('{} out of range for u8'.format(value))

        return self.data


class U16(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(2), byteorder='little')

    def encode(self, value):
        if 0 <= value <= 2 ** 16 - 1:
            self.data = ScaleBytes(bytearray(int(value).to_bytes(2, 'little')))
        else:
            raise ValueError('{} out of range for u16'.format(value))

        return self.data


class U32(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(4), byteorder='little')

    def encode(self, value):
        if 0 <= value <= 2 ** 32 - 1:
            self.data = ScaleBytes(bytearray(int(value).to_bytes(4, 'little')))
        else:
            raise ValueError('{} out of range for u32'.format(value))

        return self.data


class U64(ScaleType):

    def process(self):
        return int(int.from_bytes(self.get_next_bytes(8), byteorder='little'))

    def encode(self, value):
        if 0 <= value <= 2 ** 64 - 1:
            self.data = ScaleBytes(bytearray(int(value).to_bytes(8, 'little')))
        else:
            raise ValueError('{} out of range for u64'.format(value))

        return self.data


class U128(ScaleType):

    def process(self):
        return int(int.from_bytes(self.get_next_bytes(16), byteorder='little'))


class I8(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(1), byteorder='little', signed=True)


class I16(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(2), byteorder='little', signed=True)


class I32(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(4), byteorder='little', signed=True)


class I64(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(8), byteorder='little', signed=True)


class I128(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(16), byteorder='little', signed=True)


class I256(ScaleType):

    def process(self):
        return int.from_bytes(self.get_next_bytes(32), byteorder='little', signed=True)


class H128(ScaleType):

    def process(self):
        return '0x{}'.format(self.get_next_bytes(16).hex())


class H256(ScaleType):

    def process(self):
        return '0x{}'.format(self.get_next_bytes(32).hex())


class H512(ScaleType):

    def process(self):
        return '0x{}'.format(self.get_next_bytes(64).hex())


class VecH512Length2(ScaleType):
    type_string = '[H512; 2]'

    def process(self):
        return '0x{}'.format(self.get_next_bytes(128).hex())


class VecU8Length32(ScaleType):
    type_string = '[u8; 32]'

    def process(self):
        return '0x{}'.format(self.get_next_bytes(32).hex())


class VecU8Length16(ScaleType):
    type_string = '[u8; 16]'

    def process(self):
        value = self.get_next_bytes(16)
        try:
            return value.decode()
        except UnicodeDecodeError:
            return value.hex()


class VecU8Length8(ScaleType):
    type_string = '[u8; 8]'

    def process(self):
        value = self.get_next_bytes(8)
        try:
            return value.decode()
        except UnicodeDecodeError:
            return value.hex()


class VecU8Length4(ScaleType):
    type_string = '[u8; 4]'

    def process(self):
        value = self.get_next_bytes(4)
        try:
            return value.decode()
        except UnicodeDecodeError:
            return value.hex()


class VecU8Length2(ScaleType):
    type_string = '[u8; 2]'

    def process(self):
        value = self.get_next_bytes(2)
        try:
            return value.decode()
        except UnicodeDecodeError:
            return value.hex()


class Struct(ScaleType):

    def __init__(self, data, type_mapping=None, **kwargs):

        if type_mapping:
            self.type_mapping = type_mapping

        super().__init__(data, **kwargs)

    def process(self):

        result = {}
        for key, data_type in self.type_mapping:
            print(key)
            result[key] = self.process_type(data_type, metadata=self.metadata).value
            print(result[key])
        return result


class Era(ScaleType):

    def process(self):

        option_byte = self.get_next_bytes(1).hex()
        if option_byte == '00':
            return option_byte
        else:
            return option_byte + self.get_next_bytes(1).hex()


class EraIndex(U32):
    pass


class Bool(ScaleType):

    def process(self):
        return self.get_next_bool()


class Moment(U64):
    pass


class CompactMoment(CompactU32):
    type_string = 'Compact<Moment>'

    def process(self):
        int_value = super().process()
        if int_value < 1560000000:
            return int_value
        if int_value > 10000000000:
            int_value = int_value / 1000

        return int_value

    def serialize(self):
        return self.value


class MomentForMonth(U64):
    def process(self):
        int_value = super().process()
        return int_value

    def serialize(self):
        return self.value


class BoxProposal(ScaleType):
    type_string = 'Box<Proposal>'

    def __init__(self, data, **kwargs):
        self.call_index = None
        self.call = None
        self.call_module = None
        self.params = []
        super().__init__(data, **kwargs)

    def process(self):
        self.call_index = self.get_next_bytes(2).hex()

        self.call_module, self.call = self.metadata.call_index[self.call_index]

        for arg in self.call.args:
            arg_type_obj = self.process_type(arg.type, metadata=self.metadata)

            self.params.append({
                'name': arg.name,
                'type': arg.type,
                'value': arg_type_obj.serialize(),
                'valueRaw': arg_type_obj.raw_value
            })

        return {
            'call_index': self.call_index,
            'call_name': self.call.name,
            'call_module': self.call_module.name,
            'params': self.params
        }


class ProposalPreimage(Struct):
    type_string = '(Vec<u8>, AccountId, BalanceOf, BlockNumber)'

    type_mapping = (
        ("proposal", "HexBytes"),
        ("registredBy", "AccountId"),
        ("deposit", "BalanceOf"),
        ("blockNumber", "BlockNumber")
    )

    def process(self):
        result = {}
        for key, data_type in self.type_mapping:
            result[key] = self.process_type(data_type, metadata=self.metadata).value

        # Replace HexBytes with actual proposal
        result['proposal'] = Proposal(ScaleBytes(result['proposal']), metadata=self.metadata).decode()

        return result


class Proposal(BoxProposal):
    type_string = '<T as Trait<I>>::Proposal'


class ReferendumInfo(Struct):
    type_string = '(ReferendumInfo<BlockNumber, Proposal>)'

    type_mapping = (
        ('end', 'BlockNumber'),
        ('proposal', 'Proposal'),
        ('threshold', 'VoteThreshold'),
        ('delay', 'BlockNumber'),
    )


class ValidatorPrefs(Struct):
    type_mapping = (('unstake_threshold', 'Compact<u32>'), ('validator_payment_ratio', 'Perbill'))


class ValidatorPrefsLegacy(Struct):
    type_string = '(Compact<u32>,Compact<Balance>)'

    type_mapping = (('unstakeThreshold', 'Compact<u32>'), ('validatorPayment', 'Compact<Balance>'))


class ValidatorPrefsForDarwinia(Struct):
    type_mapping = (('unstake_threshold', 'Compact<u32>'), ('validator_payment_ratio', 'Perbill'))


class Perbill(U32):
    pass


class Linkage(Struct):
    type_string = 'Linkage<AccountId>'

    type_mapping = (
        ('previous', 'Option<AccountId>'),
        ('next', 'Option<AccountId>')
    )


class AccountId(H256):

    def process(self):
        return '0x{}'.format(self.get_next_bytes(32).hex().ljust(64, '0'))


class AccountIndex(U32):
    pass


class ReferendumIndex(U32):
    pass


class PropIndex(U32):
    pass


class Vote(U8):
    pass


class SessionKey(H256):
    pass


class SessionIndex(U32):
    pass


class AttestedCandidate(H256):
    pass


class Balance(U128):
    def process(self):
        return str(int.from_bytes(self.get_next_bytes(16), byteorder='little'))


class ParaId(U32):
    pass


class Key(Bytes):
    pass


class KeyValue(Struct):
    type_string = '(Vec<u8>, Vec<u8>)'
    type_mapping = (('key', 'Vec<u8>'), ('value', 'Vec<u8>'))


class Signature(ScaleType):

    def process(self):
        return self.get_next_bytes(64).hex()


class AuthoritySignature(ScaleType):

    def process(self):
        # TODO figure out where remaining data is missing..
        return self.get_remaining_bytes().hex()


class BalanceOf(Balance):
    pass


class BlockNumber(U32):
    pass


class NewAccountOutcome(CompactU32):
    pass


class Index(U64):
    pass


class Vec(ScaleType):

    def __init__(self, data, **kwargs):
        self.elements = []
        super().__init__(data, **kwargs)

    def process(self):
        element_count = self.process_type('Compact<u32>').value

        result = []
        for _ in range(0, element_count):
            element = self.process_type(self.sub_type, metadata=self.metadata)
            self.elements.append(element)
            result.append(element.value)

        return result


class VecNextAuthority(Vec):
    type_string = 'Vec<NextAuthority>'

    def process(self):
        element_count = self.process_type('Compact<u32>').value

        result = []
        for _ in range(0, element_count):
            element = self.process_type('NextAuthority')
            self.elements.append(element)
            result.append(element.value)

        return result


# class BalanceTransferExtrinsic(Decoder):
#
#     type_string = '(Address,Compact<Balance>)'
#
#     type_mapping = {'to': 'Address', 'balance': 'Compact<Balance>'}


class Address(ScaleType):

    def __init__(self, data, **kwargs):
        self.account_length = None
        self.account_id = None
        self.account_index = None
        self.account_idx = None
        super().__init__(data, **kwargs)

    def process(self):
        self.account_length = self.get_next_bytes(1)

        if self.account_length == b'\xff':
            self.account_id = self.get_next_bytes(32).hex()
            self.account_length = self.account_length.hex()

            return self.account_id
        else:
            if self.account_length == b'\xfc':
                account_index = self.get_next_bytes(2)
            elif self.account_length == b'\xfd':
                account_index = self.get_next_bytes(4)
            elif self.account_length == b'\xfe':
                account_index = self.get_next_bytes(8)
            else:
                account_index = self.account_length

            self.account_index = account_index.hex()
            self.account_idx = int.from_bytes(account_index, byteorder='little')

            self.account_length = self.account_length.hex()

            return self.account_index


class RawAddress(Address):
    pass


class Enum(ScaleType):
    value_list = []
    type_mapping = None

    def __init__(self, data, value_list=None, type_mapping=None, **kwargs):

        self.index = None

        if type_mapping:
            self.type_mapping = type_mapping

        if value_list:
            self.value_list = value_list

        super().__init__(data, **kwargs)

    def process(self):
        p = self.get_next_bytes(1).hex()
        if p == "":
            self.index = 0
        else:
            self.index = int(p, 16)

        if self.type_mapping:
            try:
                enum_type_mapping = self.type_mapping[self.index]
                return self.process_type('Struct', type_mapping=[enum_type_mapping]).value

            except IndexError:
                raise ValueError("Index '{}' not present in Enum type mapping".format(self.index))
        else:
            try:
                return self.value_list[self.index]
            except IndexError:
                raise ValueError("Index '{}' not present in Enum value list".format(self.index))


class Data(Enum):
    type_mapping = [
        ["None", "Null"],
        ["Raw", "Bytes"],
        ["BlakeTwo256", "H256"],
        ["Sha256", "H256"],
        ["Keccak256", "H256"],
        ["ShaThree256", "H256"]
    ]

    def process(self):
        c = self.get_next_bytes(1).hex()
        if c is "":
            return {'None': None}
        self.index = int(c, 16)
        if self.index == 0:
            return {'None': None}

        elif self.index >= 1 and self.index <= 33:
            # Determine value of Raw type (length is processed in index byte)
            data = self.get_next_bytes(self.index - 1)

            try:
                value = data.decode()
            except UnicodeDecodeError:
                value = '0x{}'.format(data.hex())
            return {"Raw": value}

        elif self.index >= 34 and self.index <= 37:

            enum_value = self.type_mapping[self.index - 32][0]

            return {enum_value: self.process_type(self.type_mapping[self.index - 32][1]).value}

        raise ValueError("Unable to decode Data, invalid indicator byte '{}'".format(self.index))


class RewardDestination(Enum):
    value_list = ['Staked', 'Stash', 'Controller']


class StakingLedger(Struct):
    type_string = 'StakingLedger<AccountId, BalanceOf, BlockNumber>'
    type_mapping = (
        ('stash', 'AccountId'),
        ('total', 'Compact<Balance>'),
        ('active', 'Compact<Balance>'),
        ('unlocking', 'Vec<UnlockChunk<Balance>>'),
    )


class UnlockChunk(Struct):
    type_string = 'UnlockChunk<Balance>'
    type_mapping = (
        ('value', 'Compact<Balance>'),
        ('era', 'Compact<EraIndex>'),
    )


class Exposure(Struct):
    type_string = 'Exposure<AccountId, BalanceOf>'
    type_mapping = (
        ('total', 'Compact<Balance>'),
        ('own', 'Compact<Balance>'),
        ('others', 'Vec<IndividualExposure<AccountId, Balance>>'),
    )


class IndividualExposure(Struct):
    type_string = 'IndividualExposure<AccountId, Balance>'
    type_mapping = (
        ('who', 'AccountId'),
        ('value', 'Compact<Balance>'),
    )


class BabeAuthorityWeight(U64):
    pass


class KeyTypeId(VecU8Length4):
    pass


class Points(U32):
    pass


class EraPoints(Struct):
    type_mapping = (
        ('total', 'Points'),
        ('individual', 'Vec<Points>'),
    )


class VoteThreshold(Enum):
    value_list = ['SuperMajorityApprove', 'SuperMajorityAgainst', 'SimpleMajority']


class Null(ScaleType):

    def process(self):
        return None


class InherentOfflineReport(Null):
    pass


class LockPeriods(U8):
    pass


class Hash(H256):
    pass


class VoteIndex(U32):
    pass


class ProposalIndex(U32):
    pass


class Permill(U32):
    pass


class ApprovalFlag(U32):
    pass


class SetIndex(U32):
    pass


class AuthorityId(H256):
    pass


class ValidatorId(H256):
    pass


class AuthorityWeight(U64):
    pass


class StoredPendingChange(Struct):
    type_mapping = (
        ('scheduled_at', 'u32'),
        ('forced', 'u32'),
    )


class OffenceDetails(Struct):
    type_mapping = (
        ('offender', 'Offender'),
        ('reporters', 'Vec<Reporter>'),
    )


class VestingSchedule(Struct):
    type_mapping = (
        ('offset', 'Balance'),
        ('perBlock', 'Balance'),
        ('startingBlock', 'BlockNumber'),
    )


class Reporter(AccountId):
    pass


class ReportIdOf(Hash):
    pass


class StorageHasher(Enum):
    value_list = ['Blake2_128', 'Blake2_256', 'Blake2_128Concat', 'Twox128', 'Twox256', 'Twox64Concat', 'Identity']


class VoterInfo(Struct):
    type_string = 'VoterInfo<Balance>'

    type_mapping = (
        ('last_active', 'VoteIndex'),
        ('last_win', 'VoteIndex'),
        ('pot', 'Balance'),
        ('stake', 'Balance'),
    )


class Gas(U64):
    pass


class CodeHash(Hash):
    pass


class PrefabWasmModule(Struct):
    type_string = 'wasm::PrefabWasmModule'

    type_mapping = (
        ('scheduleVersion', 'Compact<u32>'),
        ('initial', 'Compact<u32>'),
        ('maximum', 'Compact<u32>'),
        ('_reserved', 'Option<Null>'),
        ('code', 'Bytes'),
    )


class OpaqueNetworkState(Struct):
    type_mapping = (
        ('peerId', 'OpaquePeerId'),
        ('externalAddresses', 'Vec<OpaqueMultiaddr>'),
    )


class OpaquePeerId(Bytes):
    pass


class OpaqueMultiaddr(Bytes):
    pass


class SessionKeysSubstrate(Struct):
    type_mapping = (
        ('grandpa', 'AccountId'),
        ('babe', 'AccountId'),
        ('im_online', 'AccountId'),
    )


class SessionKeysPolkadot(Struct):
    type_mapping = (
        ('grandpa', 'AccountId'),
        ('babe', 'AccountId'),
        ('im_online', 'AccountId'),
        ('parachains', 'AccountId'),
    )


class LegacyKeys(Struct):
    type_mapping = (
        ('grandpa', 'AccountId'),
        ('babe', 'AccountId'),
    )


class EdgewareKeys(Struct):
    type_mapping = (
        ('grandpa', 'AccountId'),
    )


class QueuedKeys(Struct):
    type_string = '(ValidatorId, Keys)'

    type_mapping = (
        ('validator', 'ValidatorId'),
        ('keys', 'Keys'),
    )


class LegacyQueuedKeys(Struct):
    type_string = '(ValidatorId, LegacyKeys)'

    type_mapping = (
        ('validator', 'ValidatorId'),
        ('keys', 'LegacyKeys'),
    )


class EdgewareQueuedKeys(Struct):
    type_string = '(ValidatorId, EdgewareKeys)'

    type_mapping = (
        ('validator', 'ValidatorId'),
        ('keys', 'EdgewareKeys'),
    )


class VecQueuedKeys(Vec):
    type_string = 'Vec<(ValidatorId, Keys)>'

    def process(self):
        element_count = self.process_type('Compact<u32>').value
        result = []
        for _ in range(0, element_count):
            element = self.process_type('QueuedKeys')
            self.elements.append(element)
            result.append(element.value)

        return result


class EthereumAddress(ScaleType):

    def process(self):
        value = self.get_next_bytes(20)
        return value.hex()


class EcdsaSignature(ScaleType):

    def process(self):
        value = self.get_next_bytes(65)
        return value.hex()


class LockAmount(ScaleType):

    def process(self):
        v = self.get_next_bytes(16)
        if v.hex() == "ffffffffffffffffffffffffffffffff":
            return 0
        return int(int.from_bytes(v, byteorder='little'))


class BalanceLock(Struct):
    type_string = 'BalanceLock<Balance, BlockNumber>'

    type_mapping = (
        ('id', 'LockIdentifier'),
        ('amount', 'LockAmount'),
        ('until', 'U32'),
        ('reasons', 'WithdrawReasons'),
    )


class Set(ScaleType):
    value_list = []

    def __init__(self, data, value_list=None, **kwargs):
        self.set_value = None
        if value_list:
            self.value_list = value_list

        super().__init__(data, **kwargs)

    def process(self):
        self.set_value = self.process_type('u8').value
        result = []
        if self.set_value > 0:

            for value, set_mask in self.value_list.items():
                if self.set_value & set_mask > 0:
                    result.append(value)
        return result


class Bidder(Enum):
    type_string = 'Bidder<AccountId, ParaIdOf>'

    value_list = ['NewBidder', 'ParaId']


class BlockAttestations(Struct):
    type_mapping = (
        ('receipt', 'CandidateReceipt'),
        ('valid', 'Vec<AccountId>'),
        ('invalid', 'Vec<AccountId>'),
    )


class IncludedBlocks(Struct):
    type_mapping = (
        ('actualNumber', 'BlockNumber'),
        ('session', 'SessionIndex'),
        ('randomSeed', 'H256'),
        ('activeParachains', 'Vec<ParaId>'),
        ('paraBlocks', 'Vec<Hash>'),
    )


class CandidateReceipt(Struct):
    type_mapping = (
        ('parachainIndex', 'ParaId'),
        ('collator', 'AccountId'),
        ('signature', 'CollatorSignature'),
        ('headData', 'HeadData'),
        ('balanceUploads', 'Vec<BalanceUpload>'),
        ('egressQueueRoots', 'Vec<EgressQueueRoot>'),
        ('fees', 'u64'),
        ('blockDataHash', 'Hash'),
    )


class CollatorSignature(Signature):
    pass


class HeadData(Bytes):
    pass


class Conviction(Enum):
    CONVICTION_MASK = 0b01111111
    DEFAULT_CONVICTION = 0b00000000

    value_list = ['None', 'Locked1x', 'Locked2x', 'Locked3x', 'Locked4x', 'Locked5x', 'Locked6x']


class EraRewards(Struct):
    type_mapping = (
        ('total', 'u32'),
        ('rewards', 'Vec<u32>'),
    )


class SlashJournalEntry(Struct):
    type_mapping = (
        ('who', 'AccountId'),
        ('amount', 'Balance'),
        ('ownSlash', 'Balance'),
    )


class UpwardMessage(Struct):
    type_mapping = (
        ('origin', 'ParachainDispatchOrigin'),
        ('data', 'Bytes'),
    )


class ParachainDispatchOrigin(Enum):
    value_list = ['Signed', 'Parachain']


class StoredState(Enum):
    value_list = ['Live', 'PendingPause', 'Paused', 'PendingResume']


class UncleEntryItem(Enum):
    value_list = ['InclusionHeight', 'Uncle']


class Votes(Struct):
    type_mapping = (
        ('index', 'ProposalIndex'),
        ('threshold', 'MemberCount'),
        ('ayes', 'Vec<AccountId>'),
        ('nays', 'Vec<AccountId>'),
    )


class WinningDataEntry(Struct):
    type_mapping = (
        ('AccountId', 'AccountId'),
        ('ParaIdOf', 'ParaIdOf'),
        ('BalanceOf', 'BalanceOf'),
    )


# Edgeware types
# TODO move to RuntimeConfiguration per network


class IdentityType(Bytes):
    pass


class VoteType(Enum):
    type_string = 'voting::VoteType'

    value_list = ['Binary', 'MultiOption']


class VoteOutcome(ScaleType):

    def process(self):
        return list(self.get_next_bytes(32))


class Identity(Bytes):
    pass


class ProposalTitle(Bytes):
    pass


class ProposalContents(Bytes):
    pass


class ProposalStage(Enum):
    value_list = ['PreVoting', 'Voting', 'Completed']


class ProposalCategory(Enum):
    value_list = ['Signaling']


class VoteStage(Enum):
    value_list = ['PreVoting', 'Commit', 'Voting', 'Completed']


class TallyType(Enum):
    type_string = 'voting::TallyType'

    value_list = ['OnePerson', 'OneCoin']


class Attestation(Bytes):
    pass


# Joystream types
# TODO move to RuntimeConfiguration per network

class ContentId(H256):
    pass


class MemberId(U64):
    pass


class PaidTermId(U64):
    pass


class SubscriptionId(U64):
    pass


class SchemaId(U64):
    pass


class DownloadSessionId(U64):
    pass


class UserInfo(Struct):
    type_mapping = (
        ('handle', 'Option<Vec<u8>>'),
        ('avatar_uri', 'Option<Vec<u8>>'),
        ('about', 'Option<Vec<u8>>')
    )


class Role(Enum):
    value_list = ['Storage']


class ContentVisibility(Enum):
    value_list = ['Draft', 'Public']


class ContentMetadata(Struct):
    type_mapping = (
        ('owner', 'AccountId'),
        ('added_at', 'BlockAndTime'),
        ('children_ids', 'Vec<ContentId>'),
        ('visibility', 'ContentVisibility'),
        ('schema', 'SchemaId'),
        ('json', 'Vec<u8>'),

    )


class ContentMetadataUpdate(Struct):
    type_mapping = (
        ('children_ids', 'Option<Vec<ContentId>>'),
        ('visibility', 'Option<ContentVisibility>'),
        ('schema', 'Option<SchemaId>'),
        ('json', 'Option<Vec<u8>>')
    )


class LiaisonJudgement(Enum):
    value_list = ['Pending', 'Accepted', 'Rejected']


class BlockAndTime(Struct):
    type_mapping = (
        ('block', 'BlockNumber'),
        ('time', 'Moment')
    )


class DataObjectTypeId(U64):
    type_string = "<T as DOTRTrait>::DataObjectTypeId"


class DataObject(Struct):
    type_mapping = (
        ('owner', 'AccountId'),
        ('added_at', 'BlockAndTime'),
        ('type_id', 'DataObjectTypeId'),
        ('size', 'u64'),
        ('liaison', 'AccountId'),
        ('liaison_judgement', 'LiaisonJudgement'),
        ('ipfs_content_id', 'Bytes'),
    )


class DataObjectStorageRelationshipId(U64):
    pass


class IPNSIdentity(Bytes):
    pass


class AccountInfo(Struct):
    type_string = 'AccountInfo<BlockNumber>'

    type_mapping = (
        ('identity', 'IPNSIdentity'),
        ('expires_at', 'BlockNumber'),
    )


class DownloadState(Enum):
    value_list = ['Started', 'Ended']


class DownloadSession(Struct):
    type_mapping = (
        ('content_id', 'ContentId'),
        ('consumer', 'AccountId'),
        ('distributor', 'AccountId'),
        ('initiated_at_block', 'BlockNumber'),
        ('initiated_at_time', 'BlockNumber'),
        ('state', 'DownloadState'),
        ('transmitted_bytes', 'u64'),
    )


class Url(Bytes):
    pass


class EntryMethod(Enum):
    value_list = ['Paid', 'Screening']


class Profile(Struct):
    type_mapping = (
        ('id', 'MemberId'),
        ('handle', 'Bytes'),
        ('avatar_uri', 'Bytes'),
        ('about', 'Bytes'),
        ('registered_at_block', 'BlockNumber'),
        ('registered_at_time', 'Moment'),
        ('entry', 'EntryMethod'),
        ('suspended', 'bool'),
        ('subscription', 'Option<SubscriptionId>'),
    )


class PaidMembershipTerms(Struct):
    type_mapping = (
        ('id', 'PaidTermId'),
        ('fee', 'BalanceOf'),
        ('text', 'Bytes'),
    )


class ThreadId(U64):
    pass


class InputValidationLengthConstraint(Struct):
    type_mapping = (
        ('min', 'u16'),
        ('max_min_diff', 'u16'),
    )


class BlockchainTimestamp(Struct):
    type_string = 'BlockchainTimestamp<BlockNumber, Moment>'

    type_mapping = (
        ('block', 'BlockNumber'),
        ('time', 'Moment'),
    )


class ModerationAction(Struct):
    type_mapping = (
        ('moderated_at', 'BlockchainTimestamp<BlockNumber, Moment>'),
        ('moderator_id', 'AccountId'),
        ('rationale', 'Vec<u8>'),
    )


class PostId(U64):
    pass


class PostTextChange(Struct):
    type_string = 'PostTextChange<BlockNumber, Moment>'

    type_mapping = (
        ('expired_at', 'BlockchainTimestamp<BlockNumber, Moment>'),
        ('text', 'Vec<u8>'),
    )


class Post(Struct):
    type_string = 'Post<BlockNumber, Moment, AccountId>'

    type_mapping = (
        ('id', 'PostId'),
        ('thread_id', 'ThreadId'),
        ('nr_in_thread', 'u32'),
        ('current_text', 'Vec<u8>'),
        ('moderation', 'Option<ModerationAction<BlockNumber, Moment, AccountId>>'),
        ('text_change_history', 'Vec<PostTextChange<BlockNumber, Moment>>'),
        ('created_at', 'BlockchainTimestamp<BlockNumber, Moment>'),
        ('author_id', 'AccountId'),

    )


class Thread(Struct):
    type_string = 'Thread<BlockNumber, Moment, AccountId>'

    type_mapping = (
        ('id', 'ThreadId'),
        ('title', 'Vec<u8>'),
        ('category_id', 'CategoryId'),
        ('nr_in_category', 'u32'),
        ('moderation', 'Option<ModerationAction<BlockNumber, Moment, AccountId>>'),
        ('num_unmoderated_posts', 'u32'),
        ('num_moderated_posts', 'u32'),
        ('author_id', 'AccountId'),
        ('created_at', 'BlockchainTimestamp<BlockNumber, Moment>'),
        ('author_id', 'AccountId'),
    )


class CategoryId(U64):
    pass


class ChildPositionInParentCategory(Struct):
    type_mapping = (
        ('parent_id', 'CategoryId'),
        ('child_nr_in_parent_category', 'u32'),
    )


class Category(Struct):
    type_string = 'Category<BlockNumber, Moment, AccountId>'

    type_mapping = (
        ('id', 'CategoryId'),
        ('title', 'Vec<u8>'),
        ('description', 'Vec<u8>'),
        ('created_at', 'BlockchainTimestamp<BlockNumber, Moment>'),
        ('deleted', 'bool'),
        ('archived', 'bool'),
        ('num_direct_subcategories', 'u32'),
        ('num_direct_unmoderated_threads', 'u32'),
        ('num_direct_moderated_threads', 'u32'),
        ('position_in_parent_category', 'Option<ChildPositionInParentCategory>'),
        ('moderator_id', 'AccountId'),
    )


class ProposalStatus(Enum):
    value_list = ['Active', 'Cancelled', 'Expired', 'Approved', 'Rejected', 'Slashed']


class VoteKind(Enum):
    value_list = ['Abstain', 'Approve', 'Reject', 'Slash']


class RuntimeUpgradeProposal(Struct):
    type_string = 'RuntimeUpgradeProposal<AccountId, Balance, BlockNumber, Hash>'

    type_mapping = (
        ('id', 'u32'),
        ('proposer', 'AccountId'),
        ('stake', 'Balance'),
        ('name', 'Vec<u8>'),
        ('description', 'Vec<u8>'),
        ('wasm_hash', 'Hash'),
        ('proposed_at', 'BlockNumber'),
        ('status', 'ProposalStatus'),
    )


class TallyResult(Struct):
    type_string = 'TallyResult<BlockNumber>'

    type_mapping = (
        ('proposal_id', 'u32'),
        ('abstentions', 'u32'),
        ('approvals', 'u32'),
        ('rejections', 'u32'),
        ('slashes', 'u32'),
        ('status', 'ProposalStatus'),
        ('finalized_at', 'BlockNumber'),
    )


# Robonomics types
# TODO move to RuntimeConfiguration per network

class Order(Struct):
    type_string = 'Order<Balance, AccountId>'

    type_mapping = (
        ('models', 'Vec<u8>'),
        ('objective', 'Vec<u8>'),
        ('cost', 'Balance'),
        ('custodian', 'AccountId'),
    )


class Offer(Struct):
    type_string = 'Offer<Balance, AccountId>'

    type_mapping = (
        ('order', 'Order<Balance, AccountId>'),
        # ('sender', 'AccountId'),
    )


class Demand(Struct):
    type_string = 'Demand<Balance, AccountId>'

    type_mapping = (
        ('order', 'Order<Balance, AccountId>'),
        # ('sender', 'AccountId'), TODO not present in current blocks but referenced in https://github.com/airalab/substrate-node-robonomics/blob/master/res/custom_types.json
    )


class Liability(Struct):
    type_string = 'Liability<Balance, AccountId>'

    type_mapping = (
        ('order', 'Order<Balance, AccountId>'),
        ('promisee', 'AccountId'),
        # ('promisor', 'AccountId'), TODO not present in current blocks but referenced in https://github.com/airalab/substrate-node-robonomics/blob/master/res/custom_types.json
        ('result', 'Option<Vec<u8>>'),
    )


class LiabilityIndex(U64):
    pass


# darwinia

class TokenBalance(Balance):
    pass


class Currency(Balance):
    pass


class CurrencyOf(Balance):
    pass


class RewardBalance(Balance):
    pass


class RewardBalanceOf(Balance):
    pass


class IndividualDeposit(Struct):
    type_mapping = (
        ("month", "u32"),
        ("start_at", "u64"),
        ("value", "CurrencyOf"),
        ("balance", "TokenBalance"),
        ("claimed", "bool"),
    )


class Deposit(Struct):
    type_mapping = (
        ("total", "CurrencyOf"),
        ("deposit_list", "Vec<IndividualDeposit>"),
    )


class Keys(Struct):
    type_string = '(AccountId, AccountId)'


class ScheduleGas(Struct):
    type_mapping = (
        ("version", "u32"),
        ("putCodePerByteCost", "gas"),
        ("growMemCost", "gas"),
        ("regularOpCost", "gas"),
        ("returnDataPerByteCost", "gas"),
        ("eventDataPerByteCost", "gas"),
        ("eventPerTopicCost", "gas"),
        ("eventBaseCost", "gas"),
        ("sandboxDataReadCost", "gas"),
        ("sandboxDataWriteCost", "gas"),
        ("maxEventTopics", "u32"),
        ("maxStackHeight", "u32"),
        ("maxMemoryPages", "u32"),
        ("enablePrintln", "bool"),
        ("maxSubjectLen", "u32"),
    )


class EpochDuration(U64):
    pass


class RingBalanceOf(Balance):
    pass


class KtonBalanceOf(Balance):
    pass


class ExtendedBalance(Balance):
    pass


class IndividualExpo(Struct):
    type_mapping = (
        ("who", "AccountId"),
        ("value", "ExtendedBalance"),
    )


class RegularItem(Struct):
    type_mapping = (
        ("value", "Compact<RingBalanceOf>"),
        ("expire_time", "Compact<Moment>")
    )


class StakingBalance(Struct):
    type_string = 'StakingBalance<RingBalanceOf, KtonBalanceOf>'
    type_mapping = (
        ("value", "RingBalanceOf"),
    )

    def process(self):
        coin_key = self.process_type("Enum", value_list=['Ring', 'Kton'])
        result = {}
        for key, data_type in self.type_mapping:
            result[coin_key.value] = self.process_type(data_type).value

        return result


class TimeDepositItem(Struct):
    type_mapping = (
        ("value", "Compact<RingBalanceOf>"),
        ("start_time", "Compact<Moment>"),
        ("expire_time", "Compact<Moment>")
    )


class StakingLedgers(Struct):
    type_mapping = (
        ("stash", "AccountId"),
        ("total_ring", "Compact<RingBalanceOf>"),
        ("total_deposit_ring", "Compact<RingBalanceOf>"),
        ("active_ring", "Compact<RingBalanceOf>"),
        ("active_deposit_ring", "Compact<RingBalanceOf>"),
        ("total_kton", "Compact<KtonBalanceOf>"),
        ("active_kton", "Compact<KtonBalanceOf>"),
        ("deposit_items", "Vec<TimeDepositItem>"),
        ("unlocking", "Vec<UnlockChunk>")
    )


class Exposures(Struct):
    type_mapping = (
        ("total", "ExtendedBalance"),
        ("own", "ExtendedBalance"),
        ("others", "Vec<IndividualExpo>")
    )


class RawAuraPreDigest(Struct):
    type_mapping = (
        ("slotNumber", "u64"),
    )


class LockIdentifier(VecU8Length8):
    pass


class RawBabePreDigest(Struct):
    type_reflect = {'isPhantom': 'bool', 'Primary': 'RawBabePreDigestPrimary', 'Secondary': 'RawBabePreDigestSecondary'}

    def process(self):
        label = self.process_type("Enum", value_list=['isPhantom', 'Primary', 'Secondary']).value
        result = {label: self.process_type(self.type_reflect[label]).value}
        return result


class RawBabePreDigestPrimary(Struct):
    type_mapping = (
        ('authorityIndex', 'u32'),
        ('slotNumber', 'SlotNumber'),
        ('weight', 'BabeBlockWeight'),
        ('vrfOutput', 'H256'),
        ('vrfProof', 'H256'),
    )


class RawBabePreDigestSecondary(Struct):
    type_mapping = (
        ('authorityIndex', 'u32'),
        ('slotNumber', 'SlotNumber'),
        ('weight', 'BabeBlockWeight'),
    )


class SlotNumber(U64):
    pass


class BabeBlockWeight(U32):
    pass


class U256(ScaleType):

    def process(self):
        return int(int.from_bytes(self.get_next_bytes(32), byteorder='little'))


class H160(ScaleType):
    def process(self):
        value = self.get_next_bytes(20)
        return value.hex()


class VecU8Length256(ScaleType):
    type_string = '[u8; 256]'

    def process(self):
        return '0x{}'.format(self.get_next_bytes(256).hex())


class Call(ScaleType):
    type_string = "Box<Call>"

    def __init__(self, data, **kwargs):
        self.call_index = None
        self.call_function = None
        self.call_args = []
        self.call_module = None

        super().__init__(data, **kwargs)

    def process(self):
        self.call_index = self.get_next_bytes(2).hex()

        self.call_module, self.call_function = self.metadata.call_index[self.call_index]

        for arg in self.call_function.args:
            arg_type_obj = self.process_type(arg.type, metadata=self.metadata)

            self.call_args.append({
                'name': arg.name,
                'type': arg.type,
                'value': arg_type_obj.serialize(),
                'valueRaw': arg_type_obj.raw_value
            })

        return {
            'call_index': self.call_index,
            'call_function': self.call_function.name,
            'call_module': self.call_module.name,
            'call_args': self.call_args
        }

    def encode(self, value):
        # Check requirements
        if 'call_index' in value:
            self.call_index = value['call_index']

        elif 'call_module' in value and 'call_function' in value:
            # Look up call module from metadata
            for call_index, (call_module, call_function) in self.metadata.call_index.items():

                if call_module.name == value['call_module'] and call_function.name == value['call_function']:
                    self.call_index = call_index
                    self.call_module = call_module
                    self.call_function = call_function
                    break

            if not self.call_index:
                raise ValueError('Specified call module and function not found in metadata')

        elif not self.call_module or not self.call_function:
            raise ValueError('No call module and function specified')

        data = ScaleBytes(bytearray.fromhex(self.call_index))

        # Encode call params
        if len(self.call_function.args) > 0:
            for arg in self.call_function.args:
                if arg.name not in value['call_args']:
                    raise ValueError('Parameter \'{}\' not specified'.format(arg.name))
                else:
                    param_value = value['call_args'][arg.name]

                    arg_obj = self.get_decoder_class(arg.type, metadata=self.metadata)
                    data += arg_obj.encode(param_value)

        return data


class AccountIdAddress(Address):

    def process(self):
        self.account_id = self.process_type('AccountId').value.replace('0x', '')
        self.account_length = 'ff'
        return self.account_id
