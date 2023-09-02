import MyCert from 0x01

// This transaction configures a user's account
// to use the NFT contract by creating a new empty collection,
// storing it in their account storage, and publishing a capability
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