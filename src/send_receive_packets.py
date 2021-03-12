from src.LEACH_create_basics import *


def send_rec(Sensors: list[Sensor], myModel: Model, sender, receiver, PacketSize, sap, rap):
    # for senders
    # the packet will be sent only if the sender has energy left after transmission
    if Sensors[sender].E > 0:
        # Send a packet and increment counter by 1
        sap += 1
        print(f'{sender} sent packet. New energy of {sender} = {Sensors[sender].E}')
    else:
        print(f"node {Sensors[sender].id} is Dead")
        Sensors[sender].df = 1

    # for receivers
    # Energy dissipated from receivers for Receiving a packet
    Sensors[receiver].E -= (myModel.ERX + myModel.EDA) * PacketSize
    if Sensors[receiver].E > 0:
        # Received a Packet
        rap += 1
        print(f'{receiver} recieved a packet from {sender}')
        print(f'new energy of {receiver} = {Sensors[receiver].E}')
    else:
        Sensors[receiver].df = 1
        Sensors[receiver].E = 0

    return rap, sap


def start(Sensors: list[Sensor], myModel: Model, senders: list, receivers: list, srp, rrp, sdp, rdp, packet_type: str):
    sap = 0  # Send a packet or Number of sent packets
    rap = 0  # Receive a packet or Number of received packets
    if packet_type == 'Hello':
        PacketSize = myModel.HpacketLen
    else:
        PacketSize = myModel.DpacketLen

    # Energy dissipated from Sensors for Sending a packet
    # Each sender will send to each receiver
    for sender in senders:
        if Sensors[sender].E > 0:
            for receiver in receivers:
                if Sensors[receiver].E > 0:
                    print()
                    distance = sqrt(
                        pow(Sensors[sender].xd - Sensors[receiver].xd, 2) +
                        pow(Sensors[sender].yd - Sensors[receiver].yd, 2)
                    )
                    print(f"dist b/w sender: {sender} and receiver: {receiver} is: {distance}")

                    if distance > myModel.do:
                        Sensors[sender].E -= myModel.ETX * PacketSize + myModel.Emp * PacketSize * pow(distance, 4)
                        rap, sap = send_rec(Sensors, myModel, sender, receiver, PacketSize, sap, rap)

                    elif distance <= myModel.do:
                        Sensors[sender].E -= myModel.ETX * PacketSize + myModel.Efs * PacketSize * pow(distance, 4)
                        rap, sap = send_rec(Sensors, myModel, sender, receiver, PacketSize, sap, rap)

    if packet_type == 'Hello':
        srp += sap
        rrp += rap
        print(f"incremented srp by {sap} and rrp by {rap}")
    elif packet_type == 'Data':
        sdp += sap
        rdp += rap
        print(f"incremented sdp by {sap} and rdp by {rap}")

    print()
    return srp, rrp, sdp, rdp
