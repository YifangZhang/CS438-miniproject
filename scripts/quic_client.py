############ BASIC CLIENT ##################
import argparse
import asyncio
import ssl
import struct
import time

import aioquic.asyncio
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, ConnectionIdIssued, ConnectionIdRetired, ConnectionTerminated, DatagramFrameReceived, HandshakeCompleted, PingAcknowledged, ProtocolNegotiated, StopSendingReceived, StreamReset

_I = struct.Struct('!I')


class QuicClient(aioquic.asyncio.QuicConnectionProtocol):

    def quic_event_received(self, quic_event):
        #print(quic_event)
        # based on QuicConnectionProtocol
        # the self._quic is QuicConnection type
        #print("current original destination cid: ")
        #print(self._original_destination_connection_id)
        #print("current event is: ")
        if isinstance(quic_event, StreamDataReceived):
            #print("Stream Data Received") # too much trigger
            if quic_event.end_stream:
                self.time.set_result(self._loop.time() - self.start_time)
        elif isinstance(quic_event, ConnectionIdIssued):
            print("Connection ID Issued")
        elif isinstance(quic_event, ConnectionIdRetired):
            print("Connection ID Retired")
        elif isinstance(quic_event, ConnectionTerminated):
            print("Connection ID Terminated")
        elif isinstance(quic_event, DatagramFrameReceived):
            print("Datagram Frame Received")
        elif isinstance(quic_event, HandshakeCompleted):
            print("Handshake Completed")
        elif isinstance(quic_event, PingAcknowledged):
            print("Ping Acknowledged")
        elif isinstance(quic_event, ProtocolNegotiated):
            print("Protocol Negotiated")
        elif isinstance(quic_event, StopSendingReceived):
            print("Stop Sending Received")
        elif isinstance(quic_event, StreamReset):
            print("Stream Reset")
        else:
            print("unknown event!")

    def transfer(self, size):
        self._quic.send_stream_data(
            stream_id=self._quic.get_next_available_stream_id(),
            data=_I.pack(size),
            end_stream=True,
        )
        self.transmit()
        self.start_time = self._loop.time()
        self.time = self._loop.create_future()
        return self.time


async def main(host='192.168.1.2', port=9999, size=1048576):
    async with aioquic.asyncio.connect(
        host, port,
        configuration=QuicConfiguration(verify_mode=ssl.CERT_NONE),
        create_protocol=QuicClient,
    ) as client:
        print('Transfer speed: {:.3f} ms'.format(
           await client.transfer(size))
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('size', nargs='?', type=int, default=64, help='Transfer size (MiB)')
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    
    myport = 9999
    if(args.port is not None):
        myport = args.port
    
    asyncio.run(
        main(
            size=args.size * 1048576,
            host=args.host,
            port=myport
        )
    )
    
