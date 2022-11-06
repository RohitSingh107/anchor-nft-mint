import asyncio
import json
import os

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

LAMPORTS_PER_SOL = 1000000000


TOKEN_METADATA_PROGRAM_ID = PublicKey(
    "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s")


def create_keypair_from_file(file_path : str) -> Keypair:
    ## Generate a account (keypair) to transact with our program
    with open(file_path, 'r') as f:
        secret_key = json.load(f)
    return Keypair.from_secret_key(bytes(secret_key))


async def main():

    sale_amount = int(0.5 * LAMPORTS_PER_SOL)
    mint = PublicKey("CUu2Wvc2wH7f9QqS6SMNV2QFHMdDrxweqieSGMHynt7T")

    buyer : Keypair = create_keypair_from_file(os.getcwd() + '/tests/keypairs/buyer1.json') 



    client = AsyncClient("https://api.devnet.solana.com")
    provider = Provider(client, Wallet.local())
    # load the Program .
    program = await Program.at(
        program_id.PROGRAM_ID, provider
    )

    print(f"Program name is {program.idl.name}")

    wallet = Wallet.local()
    print(f"using wallet : {wallet.public_key}")


    owner_token_address = get_associated_token_address(
        wallet.public_key, mint)
    buyer_token_address = get_associated_token_address(
        buyer.public_key, mint)

    print(f"Request to sell NFT: {mint} for {sale_amount} lamports.")
    print(f"Owner's token address is {owner_token_address}")
    print(f"Buyer's Token address is {buyer_token_address}")



    sell = program.rpc["sell"]

    ctx = Context(accounts={
        "mint": mint,
        "owner_token_account": owner_token_address,
        "owner_authority": wallet.public_key,
        "buyer_token_account": buyer_token_address,
        "buyer_authority" : buyer.public_key,
        "rent": SYSVAR_RENT_PUBKEY,
        "system_program": system_program.SYS_PROGRAM_ID,
        "token_program": TOKEN_PROGRAM_ID,
        "associated_token_program": ASSOCIATED_TOKEN_PROGRAM_ID

    }, signers=[buyer])

    # await sell(FormatField('<', "Q").build(sale_amount), ctx = ctx)
    await sell(sale_amount, ctx = ctx)

    await program.close()

asyncio.run(main())
