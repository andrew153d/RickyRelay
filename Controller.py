import customtkinter as ctk
import serial
import serial.tools.list_ports

# Global variable to store the serial connection
serial_connection = None

# Function to send commands to the device
def send_command(command):
    global serial_connection
    try:
        if serial_connection and serial_connection.is_open:
            serial_connection.write(command.encode())
            print(f"Sent command: {command}")
        else:
            print("Serial connection not established.")
    except serial.SerialException as e:
        print(f"Error communicating with device: {e}")

# Function to turn Relay A ON
def relay_a_on():
    send_command("AON")

# Function to turn Relay A OFF
def relay_a_off():
    send_command("AOFF")

# Function to turn Relay B ON
def relay_b_on():
    send_command("BON")

# Function to turn Relay B OFF
def relay_b_off():
    send_command("BOFF")

# Function to toggle connection to the selected COM port
def toggle_connection(port, button):
    global serial_connection
    try:
        if serial_connection and serial_connection.is_open:
            serial_connection.close()
            button.configure(text="Connect", fg_color="#3a7ebf")
            print("Disconnected.")
        else:
            serial_connection = serial.Serial(port, 9600, timeout=1)
            button.configure(text="Disconnect", fg_color="#bf3a3a")
            print(f"Connected to {port}")
    except serial.SerialException as e:
        print(f"Error toggling connection: {e}")

# Set up the GUI
def create_gui():
    ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

    root = ctk.CTk()
    root.title("Relay Control")

    # Set window size
    root.geometry("400x400")

    # Create a frame to organize content in a grid
    top_frame = ctk.CTkFrame(root)
    top_frame.pack(pady=10, padx=10, fill="x")

    frame = ctk.CTkFrame(root)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Dropdown for COM port selection
    available_ports = [port.device for port in serial.tools.list_ports.comports()]
    com_port_var = ctk.StringVar(value="Select COM Port")
    com_port_dropdown = ctk.CTkOptionMenu(top_frame, variable=com_port_var, values=available_ports)
    com_port_dropdown.pack(side="left", padx=5, pady=5)

    # Connect/Disconnect button
    connection_button = ctk.CTkButton(top_frame, text="Connect", fg_color="#3a7ebf", 
                                      command=lambda: toggle_connection(com_port_var.get(), connection_button))
    connection_button.pack(side="left", padx=5, pady=5)

    # Define button colors
    on_button_color = ("#7a312e", "#934949")  # Light green, darker green on hover
    off_button_color = ("#337a2e", "#4e9349")  # Light red, darker red on hover

    # Create buttons for controlling the relays and arrange them in a grid to fill the window
    relay_a_on_button = ctk.CTkButton(frame, text="Relay A ON", command=relay_a_on, 
                                      fg_color=on_button_color[0], hover_color=on_button_color[1])
    relay_a_on_button.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    relay_a_off_button = ctk.CTkButton(frame, text="Relay A OFF", command=relay_a_off, 
                                       fg_color=off_button_color[0], hover_color=off_button_color[1])
    relay_a_off_button.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    relay_b_on_button = ctk.CTkButton(frame, text="Relay B ON", command=relay_b_on, 
                                      fg_color=on_button_color[0], hover_color=on_button_color[1])
    relay_b_on_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

    relay_b_off_button = ctk.CTkButton(frame, text="Relay B OFF", command=relay_b_off, 
                                       fg_color=off_button_color[0], hover_color=off_button_color[1])
    relay_b_off_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    # Configure grid weights to make buttons fill the frame
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Start the GUI main loop
    root.mainloop()

# Run the GUI application
if __name__ == "__main__":
    create_gui()
