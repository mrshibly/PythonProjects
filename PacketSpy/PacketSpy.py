import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from scapy.all import sniff, IP, TCP, UDP, ICMP, wrpcap
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv

class EnhancedPacketSnifferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Packet Sniffer")
        self.root.geometry("1200x800")
        self.sniffing = False
        self.packets = []
        self.filter = ""
        self.protocol_counts = {"TCP": 0, "UDP": 0, "ICMP": 0, "Other": 0}

        self.create_widgets()

    def create_widgets(self):
        """Setup the GUI elements."""
        # Top Frame for controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Filter:").pack(side=tk.LEFT, padx=5)
        self.filter_entry = ttk.Entry(control_frame, width=30)
        self.filter_entry.pack(side=tk.LEFT, padx=5)

        predefined_filters = ttk.Combobox(control_frame, values=["tcp", "udp", "icmp", "port 80"], width=15)
        predefined_filters.set("Select Filter")
        predefined_filters.pack(side=tk.LEFT, padx=5)
        predefined_filters.bind("<<ComboboxSelected>>", lambda e: self.set_filter(predefined_filters.get()))

        self.start_button = ttk.Button(control_frame, text="Start Sniffing", command=self.start_sniffing)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(control_frame, text="Stop Sniffing", command=self.stop_sniffing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(control_frame, text="Save Packets", command=self.save_packets, state=tk.DISABLED)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.export_button = ttk.Button(control_frame, text="Export Stats", command=self.export_statistics, state=tk.NORMAL)
        self.export_button.pack(side=tk.LEFT, padx=5)

        # Search Bar
        ttk.Label(control_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(control_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", self.search_packets)

        # Bottom Frame for Packet Display and Details
        display_frame = ttk.Frame(self.root)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Packet List Display
        self.packet_display = tk.Listbox(display_frame, height=20)
        self.packet_display.pack(fill=tk.BOTH, expand=True, side=tk.LEFT, padx=5, pady=5)
        self.packet_display.bind("<<ListboxSelect>>", self.display_packet_details)

        # Packet Details Display
        self.packet_details = scrolledtext.ScrolledText(display_frame, wrap=tk.WORD, height=20, state=tk.NORMAL)
        self.packet_details.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=5, pady=5)

        # Protocol Statistics (Visualization)
        stats_frame = ttk.Frame(self.root)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Protocol Distribution")
        self.ax.bar(self.protocol_counts.keys(), self.protocol_counts.values(), color="skyblue")
        self.canvas = FigureCanvasTkAgg(self.figure, stats_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def set_filter(self, filter_value):
        """Set filter from dropdown."""
        self.filter_entry.delete(0, tk.END)
        self.filter_entry.insert(0, filter_value)

    def start_sniffing(self):
        """Start packet sniffing."""
        self.filter = self.filter_entry.get().strip()
        self.sniffing = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.DISABLED)
        self.packet_display.delete(0, tk.END)
        self.packet_details.delete("1.0", tk.END)

        self.sniff_thread = threading.Thread(target=self.sniff_packets, daemon=True)
        self.sniff_thread.start()

    def sniff_packets(self):
        """Sniff packets in a separate thread."""
        try:
            sniff(filter=self.filter, prn=self.process_packet, stop_filter=self.should_stop_sniffing, store=True)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def process_packet(self, packet):
        """Process and display captured packets."""
        self.packets.append(packet)
        protocol = "Other"
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst

            if TCP in packet:
                protocol = "TCP"
            elif UDP in packet:
                protocol = "UDP"
            elif ICMP in packet:
                protocol = "ICMP"

            display_text = f"{protocol} | {src_ip} -> {dst_ip}"
            self.packet_display.insert(tk.END, display_text)

            self.protocol_counts[protocol] += 1
            self.update_stats()

    def should_stop_sniffing(self, packet):
        """Stop filter to end sniffing."""
        return not self.sniffing

    def stop_sniffing(self):
        """Stop packet sniffing."""
        self.sniffing = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.NORMAL)

    def save_packets(self):
        """Save captured packets to a .pcap file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".pcap",
                                                 filetypes=[("PCAP Files", "*.pcap"), ("All Files", "*.*")])
        if file_path:
            wrpcap(file_path, self.packets)
            messagebox.showinfo("Save Packets", f"Packets saved to {file_path}")

    def export_statistics(self):
        """Export protocol statistics to a CSV file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Protocol", "Packet Count"])
                for protocol, count in self.protocol_counts.items():
                    writer.writerow([protocol, count])
            messagebox.showinfo("Export Statistics", f"Statistics exported to {file_path}")

    def search_packets(self, event):
        """Search for packets matching a query."""
        query = self.search_entry.get().lower()
        self.packet_display.delete(0, tk.END)
        for packet in self.packets:
            if query in str(packet).lower():
                self.packet_display.insert(tk.END, packet.summary())

    def display_packet_details(self, event):
        """Display selected packet details."""
        selection = self.packet_display.curselection()
        if selection:
            index = selection[0]
            packet = self.packets[index]
            self.packet_details.config(state=tk.NORMAL)
            self.packet_details.delete("1.0", tk.END)
            self.packet_details.insert("1.0", packet.show(dump=True))
            self.packet_details.config(state=tk.DISABLED)

    def update_stats(self):
        """Update the protocol distribution chart."""
        self.ax.clear()
        self.ax.set_title("Protocol Distribution")
        self.ax.bar(self.protocol_counts.keys(), self.protocol_counts.values(), color="skyblue")
        self.canvas.draw()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedPacketSnifferApp(root)
    root.mainloop()
