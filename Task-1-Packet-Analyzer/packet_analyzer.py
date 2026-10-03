from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw, wrpcap
from datetime import datetime
from collections import Counter
import os


packet_count = 0
protocol_counts = Counter()


def analyze_packet(packet):
    global packet_count

    if IP not in packet:
        return

    packet_count += 1

    source_ip = packet[IP].src
    destination_ip = packet[IP].dst
    packet_size = len(packet)

    # Identify protocol
    if TCP in packet:
        protocol = "TCP"
        info = f"{packet[TCP].sport} -> {packet[TCP].dport}"
        info += f" | Flags: {packet[TCP].flags}"

    elif UDP in packet:
        protocol = "UDP"
        info = f"{packet[UDP].sport} -> {packet[UDP].dport}"

    elif ICMP in packet:
        protocol = "ICMP"
        info = "ICMP packet"

    else:
        protocol = "Other"
        info = "IP packet"

    protocol_counts[protocol] += 1

    # Safe hexadecimal payload preview
    payload_preview = "No payload"

    if Raw in packet:
        payload = bytes(packet[Raw].load)

        if payload:
            payload_preview = payload[:16].hex(" ").upper()

            if len(payload) > 16:
                payload_preview += " ..."

    timestamp = datetime.now().strftime("%H:%M:%S")

    print(
        f"{packet_count:<6}"
        f"{timestamp:<10}"
        f"{source_ip:<18}"
        f"{destination_ip:<18}"
        f"{protocol:<10}"
        f"{packet_size:<8}"
        f"{info:<27}"
        f"{payload_preview}"
    )


def print_header():
    print("\n" + "=" * 125)
    print("                    PYTHON NETWORK PACKET ANALYZER")
    print("=" * 125)

    print(
        f"{'No.':<6}"
        f"{'Time':<10}"
        f"{'Source IP':<18}"
        f"{'Destination IP':<18}"
        f"{'Protocol':<10}"
        f"{'Size':<8}"
        f"{'Ports / Info':<27}"
        f"Payload Preview"
    )

    print("-" * 125)


def print_summary():
    print("\n" + "=" * 60)
    print("                    CAPTURE SUMMARY")
    print("=" * 60)

    print(f"Total packets captured : {packet_count}")

    print("\nProtocol distribution:")

    for protocol, count in protocol_counts.most_common():
        print(f"  {protocol:<10}: {count}")

    print("=" * 60)


def main():
    print_header()

    print("\nStarting packet capture...")
    print("Capture duration: 20 seconds")
    print("Open websites or refresh pages to generate traffic.\n")

    start_time = datetime.now()

    # Capture for exactly 20 seconds
    packets = sniff(
        prn=analyze_packet,
        store=True,
        timeout=20
    )

    end_time = datetime.now()

    print("\nCapture completed automatically.")
    print(f"Started : {start_time.strftime('%H:%M:%S')}")
    print(f"Ended   : {end_time.strftime('%H:%M:%S')}")

    # Create captures directory
    os.makedirs("captures", exist_ok=True)

    filename = datetime.now().strftime(
        "captures/packet_capture_%Y%m%d_%H%M%S.pcap"
    )

    wrpcap(filename, packets)

    print_summary()

    print("\nPCAP file saved to:")
    print(f"  {filename}")

    print("\nPacket analysis completed successfully.")


if __name__ == "__main__":
    main()