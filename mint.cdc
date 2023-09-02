import MyCert from 0x01

// This transaction transfers an NFT from one user's collection
// to another user's collection.
transaction(recipient: Address, metadata: {String: String}) {

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

      log("Certificate Minted and deposited to Account 2's Collection")
    }
}