import serial
import time
import customtkinter as ctk
import serial.tools.list_ports

# Global variable for serial connection
ser = None

# Functions to get available COM ports
def get_com_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Functions to control relays
def SetRelayA(on_off):
    if on_off and ser:
        ser.write(("AON" + "\n").encode())
    elif ser:
        ser.write(("AOFF" + "\n").encode())

def SetRelayB(on_off):
    if on_off and ser:
        ser.write(("BON" + "\n").encode())
    elif ser:
        ser.write(("BOFF" + "\n").encode())

# Functions to handle button presses
def relayA_on():
    SetRelayA(True)

def relayA_off():
    SetRelayA(False)

def relayB_on():
    SetRelayB(True)

def relayB_off():
    SetRelayB(False)

# Toggle connect and disconnect functionality
def toggle_connection():
    global ser
    port = com_port_dropdown.get()

    if ser is None:  # Connect
        if port and port != "No COM ports found":
            try:
                ser = serial.Serial(port, 115200, timeout=1)
                connect_button.configure(text="Disconnect", fg_color="#FF5722", hover_color="#d64b1f")
                com_port_dropdown.configure(state="disabled")
                print(f"Connected to {port}")
            except serial.SerialException:
                print(f"Failed to connect to {port}")
        else:
            print("No valid COM port selected.")
    else:  # Disconnect
        ser.close()
        ser = None
        connect_button.configure(text="Connect", fg_color="#4CAF50", hover_color="#45a63c")
        com_port_dropdown.configure(state="normal")
        print("Disconnected.")

# Create the customtkinter GUI
def create_gui():
    # Initialize the main window with customtkinter styling
    window = ctk.CTk()
    window.title("Clicky")
    window.iconbitmap("circuit.ico")
    window.attributes('-topmost', True)
    window.geometry("400x350")

    # Configure appearance mode
    ctk.set_appearance_mode("dark")  # You can choose between "dark" or "light"
    ctk.set_default_color_theme("blue")  # You can customize the theme

    # COM port dropdown
    available_ports = get_com_ports()
    if not available_ports:
        available_ports = ["No COM ports found"]

    global com_port_dropdown
    com_port_dropdown = ctk.CTkOptionMenu(
        window,
        values=available_ports,
        width=200
    )
    com_port_dropdown.grid(row=0, column=0, padx=10, pady=10)

    # Connect/Disconnect button (toggle behavior)
    global connect_button
    connect_button = ctk.CTkButton(
        window,
        text="Connect",
        command=toggle_connection,
        width=200,
        height=10,
        corner_radius=10,
        fg_color="#4CAF50",  # Green for connect
        hover_color="#45a63c",  # Slightly darker green for hover
        text_color="white"
    )
    connect_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Relay control buttons
    button_a_on = ctk.CTkButton(
        window, 
        text="Relay A ON", 
        command=relayA_on, 
        width=180, 
        height=50, 
        corner_radius=10, 
        fg_color="#57d843", 
        hover_color="#45a63c",
        text_color="white"  # Set text color to white
    )
    button_a_on.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

    button_a_off = ctk.CTkButton(
        window, 
        text="Relay A OFF", 
        command=relayA_off, 
        width=180, 
        height=50, 
        corner_radius=10, 
        fg_color="#d84343", 
        hover_color="#a83838",
        text_color="white"  # Set text color to white
    )
    button_a_off.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")

    button_b_on = ctk.CTkButton(
        window, 
        text="Relay B ON", 
        command=relayB_on, 
        width=180, 
        height=50, 
        corner_radius=10, 
        fg_color="#57d843", 
        hover_color="#45a63c",
        text_color="white"  # Set text color to white
    )
    button_b_on.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")

    button_b_off = ctk.CTkButton(
        window, 
        text="Relay B OFF", 
        command=relayB_off, 
        width=180, 
        height=50, 
        corner_radius=10, 
        fg_color="#d84343", 
        hover_color="#a83838",
        text_color="white"  # Set text color to white
    )
    button_b_off.grid(row=3, column=1, padx=20, pady=20, sticky="nsew")

    # Configure grid to ensure buttons fill up their corner
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)

    # Start the event loop
    window.mainloop()

# Main function
if __name__ == '__main__':
    create_gui()
