import asyncio

from solana import system_program
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from solana.keypair import Keypair
from anchorpy.program.context import Context
from solana.sysvar import SYSVAR_RENT_PUBKEY

from spl.token.instructions import get_associated_token_address
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_PROGRAM_ID

from anchorpy import Program, Provider, Wallet

import program_id

NFT_TITLE = 'Rohit Special NFT!'
NFT_SYMBOL = 'RSN'
NFT_URL = 'https://raw.githubusercontent.com/RohitSingh107/anchor-nft-mint/main/assets/example.json'

TOKEN_METADATA_PROGRAM_ID = PublicKey(
    "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")

async def main():
    client = AsyncClient("https://api.devnet.solana.com")
    provider = Provider(client, Wallet.local())
    # load the Program .
    program = await Program.at(
        program_id.PROGRAM_ID, provider
    )

    print(f"Program name is {program.idl.name}")

    wallet = Wallet.local()
    print(f"using wallet : {wallet.public_key}")

    mint_keypair = Keypair()

    token_address = get_associated_token_address(
        wallet.public_key, mint_keypair.public_key)

    print(f"New Token: {mint_keypair.public_key}")
    print(f"Token address : {token_address}")

    metadata_address = PublicKey.find_program_address(seeds=["metadata".encode(
        encoding='UTF-8'), TOKEN_METADATA_PROGRAM_ID.__bytes__(), mint_keypair.public_key.__bytes__()], program_id=TOKEN_METADATA_PROGRAM_ID)[0]
    print(f"metadata_address is {metadata_address}")

    metadata_master_edition_address = PublicKey.find_program_address(seeds=["metadata".encode(encoding='UTF-8'), TOKEN_METADATA_PROGRAM_ID.__bytes__(
    ), mint_keypair.public_key.__bytes__(), "edition".encode(encoding='UTF-8')], program_id=TOKEN_METADATA_PROGRAM_ID)[0]

    print(f"metadata master address is {metadata_master_edition_address}")

    mint = program.rpc["mint"]

    ctx = Context(accounts={
        "metadata": metadata_address,
        "master_edition": metadata_master_edition_address,
        "mint": mint_keypair.public_key,
        "token_account": token_address,
        "mint_authority": wallet.public_key,
        "token_metadata_program": TOKEN_METADATA_PROGRAM_ID,
        "rent": SYSVAR_RENT_PUBKEY,
        "system_program": system_program.SYS_PROGRAM_ID,
        "token_program": TOKEN_PROGRAM_ID,
        "associated_token_program": ASSOCIATED_TOKEN_PROGRAM_ID

    }, signers=[mint_keypair])

    await mint(NFT_TITLE, NFT_SYMBOL, NFT_URL, ctx=ctx)

    await program.close()

asyncio.run(main())
