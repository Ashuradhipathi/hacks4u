import flow_py_sdk
import asyncio
async def test():
    async with flow_py_sdk.flow_client(
            host="access.devnet.nodes.onflow.org", port="9000"
    ) as client:
        block = await client.get_latest_block(
            is_sealed=False
            # or is_sealed = True can be used for retrieving sealed block
        )
        print("Block ID: {}".format(block.id.hex()))
        print("Block height: {}".format(block.height))
        print("Block timestamp: [{}]".format(block.timestamp))
asyncio.run(test())