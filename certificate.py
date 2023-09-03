from test import CreateCollection, MintCert, RetrieveMetadata, Config 
import asyncio
ctx_path = r"C:\Users\moizp\Documents\projects\certifyweb3\flow.json"

my_ctx = Config(ctx_path, acc_name='emulator-account')



def createCollection(address,name):
    new_ctx = Config(ctx_path, acc_name=name)
    print("Creating a collection of certificates")
    mycoll = CreateCollection(address)
    asyncio.run(mycoll.run(ctx=new_ctx))
    print("Collection created successfully!")


def mintCertificate(minter_address, receiver_address, metadata):
    print("Minting the certificate")
    mint= MintCert(minter_address, receiver_address, metadata)
    asyncio.run(mint.run(ctx=my_ctx))
    print("Minted the certificate!")
    
def retriveData(address,id):
    print("Retrieving...")
    obj = RetrieveMetadata(address,id)
    data = asyncio.run(obj.run(ctx=my_ctx))
    print("Data retrieved!")
    print(data)
    return data


# mintCertificate('0xf8d6e0586b0a20c7', '0xe03daebed8ca0615', {"test": "testing"})
# createCollection('0xe03daebed8ca0615','Moiz')
# retriveData('0xe03daebed8ca0615',1)