import MyCert from 0x01

// Print the NFTs owned by accounts 0x01 and 0x02.
pub fun main(account: Address) {

    // Get both public account objects
	let account = getAccount(account)

    // Find the public Receiver capability for their Collections
   
    let acctCapability = account.getCapability(MyCert.CollectionPublicPath)

    // borrow references from the capabilities

    let receiverRef = acctCapability.borrow<&{MyCert.NFTReceiver}>()
        ?? panic("Could not borrow account 2 receiver reference")

    // Print both collections as arrays of IDs

    log("Account 2 NFTs")
    log(receiverRef.getMetadata(id:2))
}