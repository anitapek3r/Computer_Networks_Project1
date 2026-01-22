# TCP/IP Encapsulation & Chat Application Project

## Overview
This project was developed as part of a Computer Networks course. It focuses on the practical implementation of the TCP/IP stack, demonstrating how application-layer data is encapsulated and transmitted across a network. 

The project consists of two main components:
1.  **Encapsulation Simulation:** Automating the creation of IPv4/TCP packets from raw data using Python.
2.  **Socket-Based Chat System:** A real-time messaging application with a central server and multiple clients, including deep traffic analysis of the TCP handshake and data flow.

---

## Project Structure
* `project_notebook.ipynb`: Jupyter Notebook containing the Python code for automated packet encapsulation.
* `group02_input.csv`: The source dataset containing HTTP-like application messages used for the simulation.
* `wireshark_part1.pcap` / `part2.pcap`: Traffic capture files documenting the successful transmission of packets and the chat application behavior.
* `project_report.pdf`: Comprehensive technical documentation including Wireshark analysis and architectural explanations.
* `database_structure_explanation.docx`: Detailed documentation of the server's in-memory data management.

---

## Tech Stack
* **Language:** Python 3.x
* **GUI Framework:** `Tkinter` (for the graphical chat interface).
* **Networking Libraries:** `Socket`, `Threading`.
* **Data Handling:** `Pandas` (for CSV processing).
* **Traffic Analysis:** Wireshark.

---

## Key Features

### 1. Packet Encapsulation Simulation
The simulation demonstrates the encapsulation process by converting raw data into structured network packets without external internet connectivity:
* **Data Parsing**: Extracts structured data from `group02_input.csv`, where each row represents a separate application message.
* **Encapsulation Logic:** * **Layer 4 (Transport):** Wraps data into **TCP segments** with custom ports and control flags (e.g., `PSH`, `ACK`).
                           * **Layer 3 (Network):** Encapsulates segments into **IPv4 packets** with designated source/destination IP addresses and TTL values.
 **Local Communication:** All traffic is generated locally over the **loopback interface** (localhost), ensuring that packets do not leave the host machine.
* **Traffic Verification:** Captures and analyzes the locally generated traffic using **Wireshark** to verify header integrity and the OSI model flow.

### 2. Multi-Client Chat System with GUI
A real-time messaging system where clients can communicate through a friendly interface:
* **Interactive UI:** Built with `Tkinter` for easy messaging and user list visualization.
* **Centralized Server:** Manages active connections using a `Dictionary` structure
* **Unicast Messaging:** Supports targeted messaging using the format `to:client_name;message`.
* **State Management:** Real-time updates of the active users list provided to all connected clients.
* **Concurrency:** Uses multi-threading to handle multiple simultaneous client connections.
* **Error Handling**: 
    * Validates if a username is provided upon login.
    * Notifies the sender if a target recipient is not online.
    * Detects and alerts on invalid message formats.
    * Gracefully manages client disconnections by updating the active user list for all remaining participants


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

## How to Run Part 2 (Client Server Chat Application)
**Prerequisites** 
* Python 3 installed
* All project files located in the same directory (server.py, client.py, clientGui.py)
* One computer with multiple terminals or multiple computers on the same local network

1. Network Configuration
Set a fixed IP address and port in the server configuration.
Ensure the client configuration uses the same IP and port as the server.
When running on a single machine, a local (loopback) address may be used.

2. Start the Server
Run the server application.
The server will start listening for incoming client connections and wait for clients to connect.

3. Start Clients
Run the clientGui application in a new terminal for each client.
When prompted, enter a unique username.
Once connected, all active clients are updated in real time.

4. Messaging
Clients can send messages to specific users using the predefined message format.
The server routes messages between clients and provides feedback for:
* Successful delivery
* Invalid message format
* Non-existing recipients

5. Client Disconnection
When a client disconnects:
* The server removes the client from the active list
* All remaining clients are notified
* The active clients list is updated automatically

6. Traffic Capture
Wireshark can be used to capture and analyze the TCP traffic generated by the chat application, including connections, message exchanges, errors, and disconnections.
