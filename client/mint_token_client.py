import asyncio

from solana import system_program
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Finalized
from solana.sysvar import SYSVAR_RENT_PUBKEY
from solana.transaction import Transaction

from spl.token.instructions import get_associated_token_address
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_PROGRAM_ID

from anchorpy import Wallet

from .instructions.mint import MintAccounts, MintArgs, mint

TOKEN_METADATA_PROGRAM_ID = PublicKey(
    "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")  # From docs
METADATA_TITLE = "Rohit Special Token"
METADATA_URL = "https://raw.githubusercontent.com/RohitSingh107/anchor-nft-mint/main/assets/example.json"
METADATA_SYMBOL = "RST"


async def main():

    wallet = Wallet.local()

    mint_keypair = Keypair()

    metadata_address = PublicKey.find_program_address(seeds=["metadata".encode(
        encoding='UTF-8'), TOKEN_METADATA_PROGRAM_ID.__bytes__(), mint_keypair.public_key.__bytes__()], program_id=TOKEN_METADATA_PROGRAM_ID)[0]
    print(f"metadata_address is {metadata_address}")

    metadata_master_edition_address = PublicKey.find_program_address(seeds=["metadata".encode(encoding='UTF-8'), TOKEN_METADATA_PROGRAM_ID.__bytes__(
    ), mint_keypair.public_key.__bytes__(), "edition".encode(encoding='UTF-8')], program_id=TOKEN_METADATA_PROGRAM_ID)[0]

    token_address = get_associated_token_address(
        wallet.public_key, mint_keypair.public_key)

    mintArgs = MintArgs(metadata_title=METADATA_TITLE,
                        metadata_symbol=METADATA_SYMBOL, metadata_url=METADATA_URL)

    accounts = MintAccounts(
        metadata=metadata_address,
        master_edition=metadata_master_edition_address,
        mint=mint_keypair.public_key,
        token_account=token_address,
        mint_authority=wallet.public_key,
        rent=SYSVAR_RENT_PUBKEY,
        system_program=system_program.SYS_PROGRAM_ID,
        token_program=TOKEN_PROGRAM_ID,
        associated_token_program=ASSOCIATED_TOKEN_PROGRAM_ID,
        token_metadata_program=TOKEN_METADATA_PROGRAM_ID
    )

    inx = mint(mintArgs, accounts)

    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()
    print(res)  # True

    txn = Transaction().add(inx)
    txn.sign(wallet.payer, mint_keypair)
    res = await client.send_transaction(txn, wallet.payer, mint_keypair)
    await client.confirm_transaction(res.value, commitment=Finalized)
    print(res)

    await client.close()

if __name__ == '__main__':
    asyncio.run(main())
