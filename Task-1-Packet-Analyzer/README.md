# Python Network Packet Analyzer

A Python-based network packet analyzer developed as part of the CODSOFT internship Task 1.

The application captures network packets from the local system, analyzes their communication details, identifies common protocols, and presents the captured information in a structured format.

## 🎯 Objective

The objective of this project is to:

- Capture packets transmitted over a network.
- Inspect packets to understand network communication.
- Identify source and destination IP addresses.
- Identify network protocols such as TCP, UDP, and ICMP.
- Display source and destination ports.
- Analyze TCP flags.
- Preview packet payload data safely in hexadecimal format.
- Generate protocol statistics.
- Save captured packets in PCAP format for further analysis.

## 🛠️ Technologies Used

- Python 3.12
- Scapy
- Npcap
- Git & GitHub

## 📂 Project Structure

```text
Task-1-Packet-Analyzer/
│
├── packet_analyzer.py
├── requirements.txt
├── README.md
│
└── captures/
    └── packet_capture_YYYYMMDD_HHMMSS.pcap