import asyncio
import json
import serial
import time
import websockets

clients = set()

async def broadcast(message):
    if clients:
        dead = set()
        
        for client in clients.copy():
            try:
                await client.send(message)
            except:
                dead.add(client)
        
        clients.difference_update(dead)
            
async def handler(websocket):
    clients.add(websocket)
    print("Client connected")
    
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)
        print("Client disconnected")
        
async def serial_reader():
    ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=115200,
        timeout=0.1,
    )
    
    while True:
        line = ser.readline().decode('utf-8').strip()

        if line:
            parts = line.split(',')
            
            ts_gateway = time.perf_counter_ns()
            
            if len(parts) == 8:
                try:
                    data = {
                        'ts_gw': ts_gateway,
                        'ts_stm32': int(parts[0]),
                        'ax': float(parts[1]),
                        'ay': float(parts[2]),
                        'az': float(parts[3]),
                        'temp': float(parts[4]),
                        'gx': float(parts[5]),
                        'gy': float(parts[6]),
                        'gz': float(parts[7]),
                    }
                    
                    await broadcast(json.dumps(data))
                    
                except ValueError:
                    pass
            
            await asyncio.sleep(0.01)

async def run_server(port=8765):
    print(f"Running WebSocket server on port {port}...")
    
    server = await websockets.serve(
        handler,
        '0.0.0.0',
        port,
    )
    
    await serial_reader()