# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: wallet_segwit.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto


class KeyType(betterproto.Enum):
    ORIGINAL = 1
    ENCRYPTED_SCRYPT_AES = 2
    DETERMINISTIC_MNEMONIC = 3
    DETERMINISTIC_KEY = 4


class KeyOutputScriptType(betterproto.Enum):
    P2PKH = 1
    P2WPKH = 2


class TransactionConfidenceType(betterproto.Enum):
    UNKNOWN = 0
    BUILDING = 1
    PENDING = 2
    NOT_IN_BEST_CHAIN = 3
    DEAD = 4
    IN_CONFLICT = 5


class TransactionConfidenceSource(betterproto.Enum):
    SOURCE_UNKNOWN = 0
    SOURCE_NETWORK = 1
    SOURCE_SELF = 2


class TransactionPool(betterproto.Enum):
    UNSPENT = 4
    SPENT = 5
    INACTIVE = 2
    DEAD = 10
    PENDING = 16
    PENDING_INACTIVE = 18


class TransactionPurpose(betterproto.Enum):
    UNKNOWN = 0
    USER_PAYMENT = 1
    KEY_ROTATION = 2
    ASSURANCE_CONTRACT_CLAIM = 3
    ASSURANCE_CONTRACT_PLEDGE = 4
    ASSURANCE_CONTRACT_STUB = 5
    RAISE_FEE = 6


class WalletEncryptionType(betterproto.Enum):
    UNENCRYPTED = 1
    ENCRYPTED_SCRYPT_AES = 2


@dataclass
class PeerAddress(betterproto.Message):
    ip_address: bytes = betterproto.bytes_field(1)
    port: int = betterproto.uint32_field(2)
    services: int = betterproto.uint64_field(3)


@dataclass
class EncryptedData(betterproto.Message):
    initialisation_vector: bytes = betterproto.bytes_field(1)
    encrypted_private_key: bytes = betterproto.bytes_field(2)


@dataclass
class DeterministicKey(betterproto.Message):
    """
    * Data attached to a Key message that defines the data needed by the BIP32
    deterministic key hierarchy algorithm.
    """

    # Random data that allows us to extend a key. Without this, we can't figure
    # out the next key in the chain and should just treat it as a regular
    # ORIGINAL type key.
    chain_code: bytes = betterproto.bytes_field(1)
    # The path through the key tree. Each number is encoded in the standard form:
    # high bit set for private derivation and high bit unset for public
    # derivation.
    path: List[int] = betterproto.uint32_field(2)
    # How many children of this key have been issued, that is, given to the user
    # when they requested a fresh key? For the parents of keys being handed out,
    # this is always less than the true number of children: the difference is
    # called the lookahead zone. These keys are put into Bloom filters so we can
    # spot transactions made by clones of this wallet - for instance when
    # restoring from backup or if the seed was shared between devices. If this
    # field is missing it means we're not issuing subkeys of this key to users.
    issued_subkeys: int = betterproto.uint32_field(3)
    lookahead_size: int = betterproto.uint32_field(4)
    # * Flag indicating that this key is a root of a following chain. This chain
    # is following the next non-following chain. Following/followed chains
    # concept is used for married keychains, where the set of keys combined
    # together to produce a single P2SH multisignature address
    is_following: bool = betterproto.bool_field(5)
    # Number of signatures required to spend. This field is needed only for
    # married keychains to reconstruct KeyChain and represents the N value from
    # N-of-M CHECKMULTISIG script. For regular single keychains it will always be
    # 1.
    sigs_required_to_spend: int = betterproto.uint32_field(6)


@dataclass
class Key(betterproto.Message):
    """
    * A key used to control Bitcoin spending. Either the private key, the
    public key or both may be present.  It is recommended that if the private
    key is provided that the public key is provided too because deriving it is
    slow. If only the public key is provided, the key can only be used to watch
    the blockchain and verify transactions, and not for spending.
    """

    type: "KeyType" = betterproto.enum_field(1)
    # Either the private EC key bytes (without any ASN.1 wrapping), or the
    # deterministic root seed. If the secret is encrypted, or this is a "watching
    # entry" then this is missing.
    secret_bytes: bytes = betterproto.bytes_field(2)
    # If the secret data is encrypted, then secret_bytes is missing and this
    # field is set.
    encrypted_data: "EncryptedData" = betterproto.message_field(6)
    # The public EC key derived from the private key. We allow both to be stored
    # to avoid mobile clients having to do lots of slow EC math on startup. For
    # DETERMINISTIC_MNEMONIC entries this is missing.
    public_key: bytes = betterproto.bytes_field(3)
    # User-provided label associated with the key.
    label: str = betterproto.string_field(4)
    # Timestamp stored as millis since epoch. Useful for skipping block bodies
    # before this point. The reason it's optional is that keys derived from a
    # parent don't have this data.
    creation_timestamp: int = betterproto.int64_field(5)
    deterministic_key: "DeterministicKey" = betterproto.message_field(7)
    # The seed for a deterministic key hierarchy.  Derived from the mnemonic, but
    # cached here for quick startup.  Only applicable to a DETERMINISTIC_MNEMONIC
    # key entry.
    deterministic_seed: bytes = betterproto.bytes_field(8)
    # Encrypted version of the seed
    encrypted_deterministic_seed: "EncryptedData" = betterproto.message_field(
        9)
    # The path to the root. Only applicable to a DETERMINISTIC_MNEMONIC key
    # entry.
    account_path: List[int] = betterproto.uint32_field(10)
    # Type of addresses (aka output scripts) to generate for receiving.
    output_script_type: "KeyOutputScriptType" = betterproto.enum_field(11)


@dataclass
class Script(betterproto.Message):
    program: bytes = betterproto.bytes_field(1)
    # Timestamp stored as millis since epoch. Useful for skipping block bodies
    # before this point when watching for scripts on the blockchain.
    creation_timestamp: int = betterproto.int64_field(2)


@dataclass
class ScriptWitness(betterproto.Message):
    data: List[bytes] = betterproto.bytes_field(1)


@dataclass
class TransactionInput(betterproto.Message):
    # Hash of the transaction this input is using.
    transaction_out_point_hash: bytes = betterproto.bytes_field(1)
    # Index of transaction output used by this input.
    transaction_out_point_index: int = betterproto.uint32_field(2)
    # Script that contains the signatures/pubkeys.
    script_bytes: bytes = betterproto.bytes_field(3)
    # Sequence number.
    sequence: int = betterproto.uint32_field(4)
    # Value of connected output, if known
    value: int = betterproto.int64_field(5)
    # script witness
    witness: "ScriptWitness" = betterproto.message_field(6)


@dataclass
class TransactionOutput(betterproto.Message):
    value: int = betterproto.int64_field(1)
    script_bytes: bytes = betterproto.bytes_field(2)
    # If spent, the hash of the transaction doing the spend.
    spent_by_transaction_hash: bytes = betterproto.bytes_field(3)
    # If spent, the index of the transaction input of the transaction doing the
    # spend.
    spent_by_transaction_index: int = betterproto.int32_field(4)


@dataclass
class TransactionConfidence(betterproto.Message):
    """
    * A description of the confidence we have that a transaction cannot be
    reversed in the future. Parsing should be lenient, since this could change
    for different applications yet we should maintain backward compatibility.
    """

    # This is optional in case we add confidence types to prevent parse errors -
    # backwards compatible.
    type: "TransactionConfidenceType" = betterproto.enum_field(1)
    # If type == BUILDING then this is the chain height at which the transaction
    # was included.
    appeared_at_height: int = betterproto.int32_field(2)
    # If set, hash of the transaction that double spent this one into oblivion. A
    # transaction can be double spent by multiple transactions in the case of
    # several inputs being re-spent by several transactions but we don't bother
    # to track them all, just the first. This only makes sense if type = DEAD.
    overriding_transaction: bytes = betterproto.bytes_field(3)
    # If type == BUILDING then this is the depth of the transaction in the
    # blockchain. Zero confirmations: depth = 0, one confirmation: depth = 1
    # etc.
    depth: int = betterproto.int32_field(4)
    broadcast_by: List["PeerAddress"] = betterproto.message_field(6)
    # Millis since epoch the transaction was last announced to us.
    last_broadcasted_at: int = betterproto.int64_field(8)
    source: "TransactionConfidenceSource" = betterproto.enum_field(7)


@dataclass
class Transaction(betterproto.Message):
    # See Wallet.java for detailed description of pool semantics
    version: int = betterproto.int32_field(1)
    hash: bytes = betterproto.bytes_field(2)
    # If pool is not present, that means either:  - This Transaction is either
    # not in a wallet at all (the proto is re-used elsewhere)  - Or it is stored
    # but for other purposes, for example, because it is the overriding
    # transaction of a double spend.  - Or the Pool enum got a new value which
    # your software is too old to parse.
    pool: "TransactionPool" = betterproto.enum_field(3)
    lock_time: int = betterproto.uint32_field(4)
    updated_at: int = betterproto.int64_field(5)
    transaction_input: List["TransactionInput"] = betterproto.message_field(6)
    transaction_output: List["TransactionOutput"] = betterproto.message_field(
        7)
    # A list of blocks in which the transaction has been observed (on any chain).
    # Also, a number used to disambiguate ordering within a block.
    block_hash: List[bytes] = betterproto.bytes_field(8)
    block_relativity_offsets: List[int] = betterproto.int32_field(11)
    # Data describing where the transaction is in the chain.
    confidence: "TransactionConfidence" = betterproto.message_field(9)
    purpose: "TransactionPurpose" = betterproto.enum_field(10)
    # Exchange rate that was valid when the transaction was sent.
    exchange_rate: "ExchangeRate" = betterproto.message_field(12)
    # Memo of the transaction. It can be used to record the memo of the payment
    # request that initiated the transaction.
    memo: str = betterproto.string_field(13)


@dataclass
class ScryptParameters(betterproto.Message):
    """
    * The parameters used in the scrypt key derivation function.  The default
    values are taken from http://www.tarsnap.com/scrypt/scrypt-slides.pdf.
    They can be increased - n is the number of iterations performed and  r and
    p can be used to tweak the algorithm - see:
    http://stackoverflow.com/questions/11126315/what-are-optimal-scrypt-work-
    factors
    """

    salt: bytes = betterproto.bytes_field(1)
    n: int = betterproto.int64_field(2)
    r: int = betterproto.int32_field(3)
    p: int = betterproto.int32_field(4)


@dataclass
class Extension(betterproto.Message):
    """* An extension to the wallet"""

    id: str = betterproto.string_field(1)
    data: bytes = betterproto.bytes_field(2)
    # If we do not understand a mandatory extension, abort to prevent data loss.
    # For example, this could be applied to a new type of holding, such as a
    # contract, where dropping of an extension in a read/write cycle could cause
    # loss of value.
    mandatory: bool = betterproto.bool_field(3)


@dataclass
class Tag(betterproto.Message):
    """
    * A simple key->value mapping that has no interpreted content at all. A bit
    like the extensions mechanism except an extension is keyed by the ID of a
    piece of code that's loaded with the given data, and has the concept of
    being mandatory if that code isn't found. Whereas this is just a blind
    key/value store.
    """

    tag: str = betterproto.string_field(1)
    data: bytes = betterproto.bytes_field(2)


@dataclass
class Wallet(betterproto.Message):
    """* A bitcoin wallet"""

    network_identifier: str = betterproto.string_field(1)
    # The SHA256 hash of the head of the best chain seen by this wallet.
    last_seen_block_hash: bytes = betterproto.bytes_field(2)
    # The height in the chain of the last seen block.
    last_seen_block_height: int = betterproto.uint32_field(12)
    last_seen_block_time_secs: int = betterproto.int64_field(14)
    key: List["Key"] = betterproto.message_field(3)
    transaction: List["Transaction"] = betterproto.message_field(4)
    watched_script: List["Script"] = betterproto.message_field(15)
    encryption_type: "WalletEncryptionType" = betterproto.enum_field(5)
    encryption_parameters: "ScryptParameters" = betterproto.message_field(6)
    # The version number of the wallet - used to detect wallets that were
    # produced in the future (i.e. the wallet may contain some future format this
    # protobuf or parser code does not know about). A version that's higher than
    # the default is considered from the future.
    version: int = betterproto.int32_field(7)
    extension: List["Extension"] = betterproto.message_field(10)
    # A UTF8 encoded text description of the wallet that is intended for end user
    # provided text.
    description: str = betterproto.string_field(11)
    # UNIX time in seconds since the epoch. If set, then any keys created before
    # this date are assumed to be no longer wanted. Money sent to them will be
    # re-spent automatically to the first key that was created after this time.
    # It can be used to recover a compromised wallet, or just as part of
    # preventative defence-in-depth measures.
    key_rotation_time: int = betterproto.uint64_field(13)
    tags: List["Tag"] = betterproto.message_field(16)


@dataclass
class ExchangeRate(betterproto.Message):
    """* An exchange rate between Bitcoin and some fiat currency."""

    # This much of satoshis (1E-8 fractions)…
    coin_value: int = betterproto.int64_field(1)
    # …is worth this much of fiat (1E-4 fractions).
    fiat_value: int = betterproto.int64_field(2)
    # ISO 4217 currency code (if available) of the fiat currency.
    fiat_currency_code: str = betterproto.string_field(3)
