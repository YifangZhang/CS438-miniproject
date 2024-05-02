# #####################BASIC SERVER ####################

import argparse
import asyncio
import struct

import aioquic.asyncio
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import StreamDataReceived, ConnectionIdIssued, ConnectionIdRetired, ConnectionTerminated, DatagramFrameReceived, HandshakeCompleted, PingAcknowledged, ProtocolNegotiated, StopSendingReceived, StreamReset

_I = struct.Struct('!I')


class QuicServer(aioquic.asyncio.QuicConnectionProtocol):

    def quic_event_received(self, quic_event):
        if isinstance(quic_event, StreamDataReceived):
            print("Stream Data Received")
            size, = _I.unpack(quic_event.data)
            self._quic.send_stream_data(
                stream_id=quic_event.stream_id,
                data=b'\x00' * size,
                end_stream=True,
            )
            print("data received: " + str(size))
            self.transmit()
        elif isinstance(quic_event, ConnectionIdIssued):
            print("Connection ID Issued")
            print(quic_event.connection_id)
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


async def main(certfile, keyfile=None, password=None, host="192.168.1.4", port=9999):
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile=certfile, keyfile=keyfile, password=password)
    server = await aioquic.asyncio.serve(
        host, port,
        configuration=configuration,
        create_protocol=QuicServer,
    )

    loop = asyncio.get_running_loop()
    try:
        await loop.create_future()
    finally:
        server.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--certificate', required=True)
    parser.add_argument('-k', '--private-key')
    parser.add_argument('-j', '--json')
    parser.add_argument('--host', type=str, required=True)
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()

    cert = None
    pkey = None

    if(args.json is not None):
        import json
        with open(str(args.json), "r") as fp:
            myCA = json.load(fp)
            cert = myCA['myCA_pem']
            pkey = myCA['myCA_key']

    else:
        cert = args.certificate
        pkey = args.private_key

    mypw = "Abcd1234"
    
    myport = 9999
    if(args.port is not None):
        myport = args.port
    
    asyncio.run(
        main(
            certfile=cert,
            keyfile=pkey,
            password=mypw,
            host=args.host,
            port=myport
        )
    )
