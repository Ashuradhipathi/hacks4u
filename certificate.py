from test import CreateCollection, MintCert, RetrieveMetadata, Config 
import asyncio
ctx_path = r"C:\Users\moizp\Documents\projects\certifyweb3\flow.json"

my_ctx = Config(ctx_path)


address = input("Enter the Flow account address: ")


def createCollection(address):
    print("Creating a collection of certificates")
    mycoll = CreateCollection(address)
    asyncio.run(mycoll.run(ctx=my_ctx))
    print("Collection created successfully!")


def mintCertificate(minter_address, receiver_address, metadata):
    print("Minting the certificate")
    mint= MintCert(minter_address, receiver_address, metadata)
    asyncio.run(mint.run(ctx=my_ctx))
    print("Minted the certificate!")
    
def retriveData(address):
    print("Retrieving...")
    obj = RetrieveMetadata(address)
    data = asyncio.run(obj.run(ctx=my_ctx))
    print("Data retrieved!")
    return data

# mintCertificate('0xe03daebed8ca0615')