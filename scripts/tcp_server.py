import asyncio
import argparse
import struct

_I = struct.Struct('!I')

async def handle_echo(reader, writer):
    data = await reader.read(1024)
    #message = data.decode()
    
    print("Stream Data Received")
    size, = _I.unpack(data)
    addr = writer.get_extra_info('peername')
    
    print(f"Received {size!r} from {addr!r}")

    #print(f"Send: {message!r}")
    message = b'\x00' * size
    writer.write(message)
    await writer.drain()

    print("Close the connection")
    writer.close()
    await writer.wait_closed()

async def main(host, port):
    server = await asyncio.start_server(
        handle_echo, host, port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('size', nargs='?', type=int, default=64, help='Transfer size (MiB)')
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    
    #mysize = args.size * 1048576
        
    asyncio.run(main(host=args.host, port=args.port))