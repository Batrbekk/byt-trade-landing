import asyncio
from tardis_client import TardisClient, Channel

async def replay():
    tardis_client = TardisClient()

    # replay method returns Async Generator
    # https://rickyhan.com/jekyll/update/2018/01/27/python36.html
    messages = tardis_client.replay(
        exchange="bitmex",
        from_date="2022-10-20",
        to_date="2022-10-20 00:01",
        filters=[
          Channel(name="trade", symbols=["XBTUSD"])
        ],
    )

    # this will print all trades and orderBookL2 messages for XBTUSD
    # and all trades for ETHUSD for bitmex exchange
    # between 2019-06-01T00:00:00.000Z and 2019-06-02T00:00:00.000Z 
    #(whole first day of June 2019)
    async for local_timestamp, message in messages:
        # local timestamp is a Python datetime that marks timestamp 
        # when given message has been received
        # message is a message object as provided by exchange real-time stream
        print(message)

asyncio.run(replay())