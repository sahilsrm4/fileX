import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():

    async with streamable_http_client(
        "http://localhost:8931/mcp"
    ) as (read_stream, write_stream):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.list_tools()

            for tool in result.tools:
                print(tool.name)
                print(tool.description)
                print(tool.input_schema)
                print("-" * 50)


asyncio.run(main())