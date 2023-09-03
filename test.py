from flow_py_sdk import flow_client, ProposalKey, Tx, Script
import json
import logging
from pathlib import Path
import asyncio
from flow_py_sdk.cadence import Address, Dictionary, String, KeyValuePair, UInt64, Struct,Value
from flow_py_sdk.signer import InMemorySigner, HashAlgo, SignAlgo
from typing import List


log = logging.getLogger(__name__)


class Config(object):
    def __init__(self, config_location: Path, acc_name) -> None:
        super().__init__()
        self.acc_name: acc_name

        self.access_node_host: str = "localhost"
        self.access_node_port: int = 3569

        self.service_account_key_id: int = 0
        # noinspection PyBroadException
        try:
            with open(config_location) as json_file:
                data = json.load(json_file)
                self.service_account_address = Address.from_hex(
                    data["accounts"][acc_name]["address"]
                )
                self.service_account_signer = InMemorySigner(
                    hash_algo=HashAlgo.SHA3_256,
                    sign_algo=SignAlgo.ECDSA_P256,
                    private_key_hex=data["accounts"][acc_name]["key"],
                )
        except Exception:
            log.warning(
                f"Cannot open {config_location}, using default settings",
                exc_info=True,
                stack_info=True,
            )

class CreateCollection():
    def __init__(self, account: Address):
        self.account_address = Address.from_hex(account)
    async def run(self, ctx: Config):
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account = await client.get_account(address=self.account_address)
            account_address = self.account_address
            new_signer =ctx.service_account_signer
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )

            transaction = Tx(
                code=r"""
                import MyCert from 0xf8d6e0586b0a20c7

transaction {
    prepare(acct: AuthAccount) {

        // Create a new empty collection
        let collection <- MyCert.createEmptyCollection()

        // store the empty NFT Collection in account storage
        acct.save<@MyCert.Collection>(<-collection, to: MyCert.CollectionStoragePath)

        log("Collection created for account 2")

        // create a public capability for the Collection
        acct.link<&{MyCert.NFTReceiver}>(MyCert.CollectionPublicPath, target: MyCert.CollectionStoragePath)

        log("Capability created")
    }
}
                """,
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).add_authorizers(account_address).with_envelope_signature(
                account_address,
                0,
                new_signer,
            )

            response = await client.send_transaction(transaction=transaction.to_signed_grpc())
            transaction_id = response.id

        transaction = await client.get_transaction(id=transaction_id)
        print("transaction ID: {}".format(transaction_id.hex()))
        print("transaction payer: {}".format(transaction.payer.hex()))
        print(
            "transaction proposer: {}".format(
                transaction.proposal_key.address.hex()
            )
        )


class MintCert():
    def __init__(self, sender: Address, receiver: Address, metadata: dict):
        self.account_address = Address.from_hex(sender)
        self.receiver_address = Address.from_hex(receiver)
        kvpair= []
        for key, value in metadata.items():
            kvpair.append(KeyValuePair(String(key), String(value)))
            
        self.metadata = Dictionary(kvpair)
    async def run(self, ctx: Config):
        async with flow_client(
                host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            account = await client.get_account(address=self.account_address)
            account_address = self.account_address
            new_signer =ctx.service_account_signer
            latest_block = await client.get_latest_block()
            proposer = await client.get_account_at_latest_block(
                address=account_address.bytes
            )

            transaction = Tx(
                code=r"""
                import MyCert from 0xf8d6e0586b0a20c7

// This transaction transfers an NFT from one user's collection
// to another user's collection.
transaction(recipient: Address, metadata : {String: String}) {
    
    // The field that will hold the NFT as it is being
    // transferred to the other account
    let minterRef: &MyCert.NFTMinter
    prepare(acct: AuthAccount) {

        // Borrow a reference from the stored collection
        let collectionRef = acct.borrow<&MyCert.Collection>(from: MyCert.CollectionStoragePath)
            ?? panic("Could not borrow a reference to the owner's collection")

        // Call the withdraw function on the sender's Collection
        // to move the NFT out of the collection
        self.minterRef = acct.borrow<&MyCert.NFTMinter>(from: /storage/NFTMinter)
          ?? panic("could not borrow minter reference")
    }

    execute {
        // Get the recipient's public account object
        let recipient = getAccount(recipient)

        // Get the Collection reference for the receiver
        // getting the public capability and borrowing a reference from it
        let receiverRef = recipient.getCapability<&{MyCert.NFTReceiver}>(MyCert.CollectionPublicPath)
            .borrow()
            ?? panic("Could not borrow receiver reference")

        let newNFT <- self.minterRef.mintNFT()
         

        receiverRef.deposit(token: <-newNFT, metadata: metadata)

      log("Certificate Minted and deposited to Account's Collection")
    }
}
                """,
                reference_block_id=latest_block.id,
                payer=account_address,
                proposal_key=ProposalKey(
                    key_address=account_address,
                    key_id=0,
                    key_sequence_number=proposer.keys[0].sequence_number,
                ),
            ).add_arguments(self.receiver_address, self.metadata).add_authorizers(account_address).with_envelope_signature(
                account_address,
                0,
                new_signer,
            )

            response = await client.send_transaction(transaction=transaction.to_signed_grpc())
            transaction_id = response.id

        transaction = await client.get_transaction(id=transaction_id)
        print("transaction ID: {}".format(transaction_id.hex()))
        print("transaction payer: {}".format(transaction.payer.hex()))
        print(
            "transaction proposer: {}".format(
                transaction.proposal_key.address.hex()
            )
        )
            



class RetrieveMetadata():
    def __init__(self, receiver: Address, id: int) -> None:
        self.receiver_address = Address.from_hex(receiver)
        self.id=id

    async def run(self, ctx: Config):
        script = Script(
            code=r"""
                    import MyCert from 0xf8d6e0586b0a20c7

pub fun main(account: Address, certID: UInt64) : {String: String} {

    // Get both public account objects
	let account = getAccount(account)

    // Find the public Receiver capability for their Collections
   
    let acctCapability = account.getCapability(MyCert.CollectionPublicPath)

    // borrow references from the capabilities

    let receiverRef = acctCapability.borrow<&{MyCert.NFTReceiver}>()
        ?? panic("Could not borrow account 2 receiver reference")

    // Print both collections as arrays of IDs

    return receiverRef.getMetadata(id:certID)
}
                """,
            arguments=[self.receiver_address, UInt64(self.id)],
        )

        async with flow_client(
            host=ctx.access_node_host, port=ctx.access_node_port
        ) as client:
            complex_script = await client.execute_script(
                script=script
                # , block_id
                # , block_height
            )

            if not complex_script:
                raise Exception("Script execution failed")

            script_result: Value = complex_script
            m = script_result.as_type(Dictionary).value
            result = {}
            for obj in m:
                result[str(obj.key)]=str(obj.value)
            print(result)
            return result
            



            
# a = CreateCollection('0xe03daebed8ca0615')
# asyncio.run(a.run(ctx = Config(r"C:\Users\moizp\Documents\projects\hacks4u\flow.json", 'Moiz')))


# b = MintCert('0xf8d6e0586b0a20c7', '0xe03daebed8ca0615', {"Name": "Moiz"})

# asyncio.run(b.run(ctx = Config(r"C:\Users\moizp\Documents\projects\hacks4u\flow.json", 'emulator-account')))

# c = RetrieveMetadata('0xe03daebed8ca0615', 1)
# asyncio.run(c.run(ctx = Config(r"C:\Users\moizp\Documents\projects\hacks4u\flow.json", 'emulator-account')))