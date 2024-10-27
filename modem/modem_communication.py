import tkinter as tk
from wlmodem import WlModem
import threading
import time

class ModemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modem Command Interface")

        # Set up the modem
        self.modem = WlModem("/dev/ttyUSB0")
        if not self.modem.connect():
            print("Failed to connect to modem")

        self.modem.cmd_configure('b', 3)
        if self.modem.cmd_get_diagnostic().get("link_up"):
            print("Link is up")

        # Input field
        self.entry = tk.Entry(root, width=20)
        self.entry.pack()

        # Send button
        self.send_button = tk.Button(root, text="Send", command=self.send_command)
        self.send_button.pack()

        # Display area for received data
        self.output = tk.Text(root, height=10, width=30)
        self.output.pack()

        # Start a thread to listen for incoming data
        self.listen_thread = threading.Thread(target=self.receive_data)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send_command(self):
        command = self.entry.get().strip()
        if command in data_dict:
            data = f"{command:<2}######".encode('utf-8')  # Format to 8 characters
            success = self.modem.cmd_queue_packet(data)
            status = "Success" if success else "Failed"
            self.output.insert(tk.END, f"Sent '{command}' data: {status}\n")
        else:
            self.output.insert(tk.END, "Invalid command. Use ax, ay, az, wx, wy, wz.\n")

    def receive_data(self):
        while True:
            pkt = self.modem.get_data_packet()
            if pkt:
                self.output.insert(tk.END, f"Received: {pkt.decode('utf-8', errors='ignore')}\n")
            time.sleep(0.1)

# Example data for transmission based on commands
data_dict = {
    "ax": b"0.123", "ay": b"0.456", "az": b"0.789",
    "wx": b"1.123", "wy": b"1.456", "wz": b"1.789"
}

# Run the GUI
root = tk.Tk()
app = ModemApp(root)
root.mainloop()


