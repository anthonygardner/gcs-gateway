import argparse
import asyncio

def main():
    parser = argparse.ArgumentParser(prog='gcs-gateway')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    ws_parser = subparsers.add_parser('ws', help='Start WebSocket server')
    ws_parser.add_argument('--port', type=int, default=8765)
    
    args = parser.parse_args()
    
    if args.command == 'ws':
        from gcs_gateway.websocket_server import run_server
        asyncio.run(run_server(port=args.port))