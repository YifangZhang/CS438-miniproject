import asyncio
import argparse
import struct
import time

_I = struct.Struct('!I')

start_time = 0


#def timer_check(writer):
#    writer.wait_closed()
#    end_time = time.time()
#    print(f"the total time takes {(end_time - start_time)*1000} ms")

async def tcp_echo_client(host, port, size):
    reader, writer = await asyncio.open_connection(
        host, port)

    message = _I.pack(size)
    writer.write(message)
    await writer.drain()

    data = await reader.read(size*2)
    print("data received")
    #print(data)

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('size', nargs='?', type=int, default=64, help='Transfer size (MiB)')
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    
    mysize = args.size * 1048576
        
    start_time = time.time()
    asyncio.run(tcp_echo_client(host=args.host, port=args.port, size=mysize))
    
    end_time = time.time()
    print(f"the total time takes {(end_time - start_time)*1000} ms")
    