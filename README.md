# TCP/IP Encapsulation & Chat Application Project

## Overview
This project was developed as part of a Computer Networks course. It focuses on the practical implementation of the TCP/IP stack, demonstrating how application-layer data is encapsulated and transmitted across a network. 

The project consists of two main components:
1.  **Encapsulation Simulation:** Automating the creation of IPv4/TCP packets from raw data using Python.
2.  **Socket-Based Chat System:** A real-time messaging application with a central server and multiple clients, including deep traffic analysis of the TCP handshake and data flow.

---

## Project Structure
* `project_notebook.ipynb`: Jupyter Notebook containing the Python code for automated packet encapsulation using the **Scapy** library.
* `group02_input.csv`: The source dataset containing HTTP-like application messages used for the simulation.
* `wireshark_part1.pcap` / `part2.pcap`: Traffic capture files documenting the successful transmission of packets and the chat application behavior.
* `project_report.docx`: Comprehensive technical documentation including Wireshark analysis and architectural explanations.
* `database_structure_explanation.docx`: Detailed documentation of the server's in-memory data management.

---

## Tech Stack
* **Language:** Python 3.x
* **GUI Framework:** `Tkinter` (for the graphical chat interface).
* **Networking Libraries:** `Scapy` (for packet crafting), `Socket`, `Threading`.
* **Data Handling:** `Pandas` (for CSV processing).
* **Traffic Analysis:** Wireshark.

---

## Key Features

### 1. Packet Encapsulation Simulation
The simulation demonstrates the encapsulation process by converting raw data into structured network packets without external internet connectivity:
* **Data Source:** Parses application-layer payloads (HTTP-like messages) from a local `CSV` file.
* **Encapsulation Logic:** * **Layer 4 (Transport):** Wraps data into **TCP segments** with custom ports and control flags (e.g., `PSH`, `ACK`).
                           * **Layer 3 (Network):** Encapsulates segments into **IPv4 packets** with designated source/destination IP addresses and TTL values.
* **Local Injection:** Uses the `Scapy` library to inject these crafted packets directly into the **Loopback Interface** (localhost).
* **Traffic Verification:** Captures and analyzes the locally generated traffic using **Wireshark** to verify header integrity and the OSI model flow.

### 2. Multi-Client Chat System with GUI
A real-time messaging system where clients can communicate through a friendly interface:
* **Interactive UI:** Built with `Tkinter` for easy messaging and user list visualization.
* **Centralized Server:** Manages active connections using a `Dictionary` structure
* **Unicast Messaging:** Supports targeted messaging using the format `to:client_name;message`.
* **State Management:** Real-time updates of the active users list provided to all connected clients.
* **Concurrency:** Uses multi-threading to handle multiple simultaneous client connections.

---

## Network Analysis Insights
Through this project, we analyzed several critical network behaviors:
* **TCP 3-Way Handshake:** Observation of the `SYN` -> `SYN-ACK` -> `ACK` sequence during connection establishment.
* **Encapsulation Flow:** Verifying that the CSV data correctly appears as the "Data" payload within the TCP segment in Wireshark.
* **Connection Teardown:** Analyzing the `FIN` and `RST` flags during client disconnection.

---

## Contributors :)
* [**Anita Peker**]- (https://github.com/anitapek3r)
* [**Shir Yermiyahu**]-(https://github.com/shirjer2401-ux)
* [**Adir Beitbabu**]-(https://github.com/AdirBeitbabu)
---

## How to Run
1.  Install dependencies: `pip install scapy pandas`
2.  Run as Administrator (required for raw packet injection).
3.  Launch the Chat Server (server.py) and then the Clients (clientGui.py) to start messaging.
