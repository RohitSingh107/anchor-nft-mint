from __future__ import annotations
import typing
from solana.publickey import PublicKey
from solana.transaction import TransactionInstruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class MintArgs(typing.TypedDict):
    metadata_title: str
    metadata_symbol: str
    metadata_url: str


layout = borsh.CStruct(
    "metadata_title" / borsh.String,
    "metadata_symbol" / borsh.String,
    "metadata_url" / borsh.String,
)


class MintAccounts(typing.TypedDict):
    metadata: PublicKey
    master_edition: PublicKey
    mint: PublicKey
    token_account: PublicKey
    mint_authority: PublicKey
    rent: PublicKey
    system_program: PublicKey
    token_program: PublicKey
    associated_token_program: PublicKey
    token_metadata_program: PublicKey


def mint(
    args: MintArgs,
    accounts: MintAccounts,
    program_id: PublicKey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> TransactionInstruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["metadata"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["master_edition"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["mint"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["mint_authority"], is_signer=True, is_writable=True
        ),
        AccountMeta(pubkey=accounts["rent"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["system_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["token_program"], is_signer=False, is_writable=False
        ),
        AccountMeta(
            pubkey=accounts["associated_token_program"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["token_metadata_program"],
            is_signer=False,
            is_writable=False,
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"39\xe1/\xb6\x92\x89\xa6"
    encoded_args = layout.build(
        {
            "metadata_title": args["metadata_title"],
            "metadata_symbol": args["metadata_symbol"],
            "metadata_url": args["metadata_url"],
        }
    )
    data = identifier + encoded_args
    return TransactionInstruction(keys, program_id, data)
