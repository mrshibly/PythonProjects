# PacketSpy

**PacketSpy** is a sleek and powerful network packet-sniffing tool that lets you monitor, analyze, and explore network traffic in real-time. With advanced filtering, detailed packet inspection, and interactive visualizations, PacketSpy is your ultimate companion for understanding network behavior.

---

## Features

- 🛠️ **Packet Sniffing**: Capture live network traffic across protocols like TCP, UDP, and ICMP.
- 🔍 **Packet Analysis**: View detailed information about each packet, including headers and payloads.
- 🎛️ **Custom Filtering**: Apply filters to focus on specific traffic (e.g., `tcp`, `udp`, `port 80`).
- 📊 **Interactive Visualizations**: Real-time bar charts showing protocol distribution.
- 🔎 **Search Functionality**: Quickly search for packets based on IP, protocol, or keywords.
- 📁 **Save & Export**:
  - Save captured packets as `.pcap` files for further analysis.
  - Export protocol statistics as CSV files.
- 💡 **Predefined Filters**: Select common filters with a single click (e.g., HTTP traffic).
- 🎨 **Modern GUI**: Intuitive and responsive interface with customizable themes.

---

## Installation

1. Make sure you have **Python 3.8+** installed.
2. Install the required dependencies:
   ```bash
   pip install scapy matplotlib
   ```
3. Download the `PacketSpy` script and run it:
   ```bash
   python packetspy.py
   ```

---

## Usage

1. Launch `PacketSpy` using the command:
   ```bash
   python packetspy.py
   ```
2. Use the filter box to apply specific filters (e.g., `tcp`, `udp`, `port 80`).
3. Start sniffing packets using the **Start Sniffing** button.
4. Stop sniffing anytime and:
   - Save captured packets to a `.pcap` file.
   - Export protocol statistics as a `.csv` file.
5. Click on any packet in the list to view detailed information.

---

## Screenshots

**Main Interface:**
![Screenshot 2024-12-03 154421](https://github.com/user-attachments/assets/a0e7b93e-97aa-4912-983d-7fdebc82d0d6)

---

## Dependencies

PacketSpy uses the following libraries:
- [Scapy](https://scapy.net/): For capturing and analyzing network packets.
- [Matplotlib](https://matplotlib.org/): For real-time protocol visualizations.
- [Tkinter](https://wiki.python.org/moin/TkInter): For building the GUI.

---

## Disclaimer

**PacketSpy** is a tool designed for educational and testing purposes only. Ensure you have proper authorization before sniffing network traffic. Unauthorized use may violate privacy and legal regulations.

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve PacketSpy.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
