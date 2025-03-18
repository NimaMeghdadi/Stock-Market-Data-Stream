# import asyncio
import websockets
import json
from datetime import datetime
import logging
# WebSocket URL
URL = "wss://push.coinmarketcap.com/ws?device=web&client_source=coin_detail_page"

# Subscription message
request = {
    "method": "RSUBSCRIPTION",
    "params": ["main-site@crypto_price_15s@{}@detail", "1"]
}

ID_COIN_MAP={
    1: 'BTC',
    1027: 'ETH',
}

async def stream_data(producer):
    logging.info("Waiting for data")
    async with websockets.connect(URL) as ws:
        # Send the request
        await ws.send(json.dumps(request))
        
        # while True:
        first_message = True

        while True:
            # logging.info("Waiting for data")
            response = await ws.recv()
            if first_message:  # Skip the first message
                first_message = False
                continue
            try:
                data = json.loads(response)
            
            except json.JSONDecodeError as e:
                logging.error("Failed to parse JSON: %s", e)
                
            data = json.loads(response)
            stock_data = {
                'symbol': ID_COIN_MAP[data['d']['id']],
                'price': data['d']['p'],
                'timestamp': datetime.fromtimestamp(int(data['t'])/1000).isoformat()
            }
            logging.info("Received data: %s", stock_data)
            producer.send(stock_data)
