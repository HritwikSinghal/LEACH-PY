from src.LEACH_create_basics import *


def send_rec(Sensors: list[Sensor], sender, sap):
    # for senders
    # the packet will be sent only if the sender has energy left after transmission
    if Sensors[sender].E > 0:
        # Send a packet and increment counter by 1
        sap += 1
        print(f'{sender} sent packet. New energy of {sender} = {Sensors[sender].E}')
    else:
        print(f"node {Sensors[sender].id} is Dead! :( look how they massacred my node.")
        Sensors[sender].df = 1

    return sap


def start(Sensors: list[Sensor], my_model: Model, senders: list, receivers: list, srp, rrp, sdp, rdp, packet_type: str):
    sent_packets = 0  # Number of sent packets
    rec_packets = 0  # Number of received packets

    PacketSize = my_model.hello_packet_len if packet_type == 'Hello' else my_model.data_packet_len

    # todo: do not increment rdp and/or sdp if one of them is dead

    # Energy dissipated from Sensors for Sending a packet
    # Each sender will send to each receiver
    for sender in senders:
        for receiver in receivers:
            print("########sender is ", sender, "and rec is ", receiver)
            print()
            distance = sqrt(
                pow(Sensors[sender].xd - Sensors[receiver].xd, 2) +
                pow(Sensors[sender].yd - Sensors[receiver].yd, 2)
            )
            print(f"dist b/w sender: {sender} and receiver: {receiver} is: {distance}")

            if distance > my_model.do:
                Sensors[sender].E -= my_model.ETX * PacketSize + my_model.Emp * PacketSize * pow(distance, 4)
                sent_packets = send_rec(Sensors, sender, sent_packets)

            else:
                Sensors[sender].E -= my_model.ETX * PacketSize + my_model.Efs * PacketSize * pow(distance, 2)
                sent_packets = send_rec(Sensors, sender, sent_packets)

    for receiver in receivers:
        Sensors[receiver].E -= (my_model.ERX + my_model.EDA) * PacketSize

    # for receivers
    # Energy dissipated from receivers for Receiving a packet, if the sender died during transmission,
    # the energy of receiver will be wasted but it will not receive any packet
    for sender in senders:
        for receiver in receivers:
            if Sensors[receiver].E > 0 and Sensors[sender].E > 0:
                # Received a Packet
                rec_packets += 1
                print(f'{receiver} received a packet, new energy of {receiver} = {Sensors[receiver].E}')
            elif Sensors[receiver].E < 0:
                Sensors[receiver].df = 1

    if packet_type == 'Hello':
        srp += sent_packets
        rrp += rec_packets
        print(f"incremented srp by {sent_packets} and rrp by {rec_packets}")
    elif packet_type == 'Data':
        sdp += sent_packets
        rdp += rec_packets
        print(f"incremented sdp by {sent_packets} and rdp by {rec_packets}")

    print()
    return srp, rrp, sdp, rdp
