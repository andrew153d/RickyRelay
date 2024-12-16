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

# Functions to handle slider changes
def relayA_slider_change(value):
    value = float(value)
    if value == 1.0:
        SetRelayA(True)
    else:
        SetRelayA(False)
    update_slider_fill(relayA_slider_canvas, value)

def relayB_slider_change(value):
    value = float(value)
    if value == 1.0:
        SetRelayB(True)
    else:
        SetRelayB(False)
    update_slider_fill(relayB_slider_canvas, value)

# Function to update the slider fill color and width
def update_slider_fill(canvas, value):
    fill_color = "green" if value == 1.0 else "red"
    fill_width = int(value * 300)  # 300px is the total width of the slider
    canvas.delete("fill")  # Clear the previous fill
    canvas.create_rectangle(0, 0, fill_width, 40, fill=fill_color, tags="fill")  # Draw the new fill

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

    # Relay A slider - Canvas for rectangle
    global relayA_slider_canvas
    relayA_slider_canvas = ctk.CTkCanvas(
        window, 
        width=300, height=40, 
        bg="gray", bd=0, highlightthickness=0
    )
    relayA_slider_canvas.grid(row=2, column=0, padx=20, pady=20)
    relayA_slider_canvas.create_rectangle(0, 0, 0, 40, fill="red", tags="fill")  # Initial red fill
    
    # Relay B slider - Canvas for rectangle
    global relayB_slider_canvas
    relayB_slider_canvas = ctk.CTkCanvas(
        window, 
        width=300, height=40, 
        bg="gray", bd=0, highlightthickness=0
    )
    relayB_slider_canvas.grid(row=3, column=0, padx=20, pady=20)
    relayB_slider_canvas.create_rectangle(0, 0, 0, 40, fill="red", tags="fill")  # Initial red fill

    # Relay A slider (for controlling state)
    relayA_slider = ctk.CTkSlider(
        window,
        from_=0, to=1,
        number_of_steps=2,  # Two positions: off (0) and on (1)
        command=relayA_slider_change,
        width=300
    )
    relayA_slider.set(0)  # Default to off
    relayA_slider.grid(row=2, column=1, padx=20, pady=20)

    # Relay B slider (for controlling state)
    relayB_slider = ctk.CTkSlider(
        window,
        from_=0, to=1,
        number_of_steps=2,  # Two positions: off (0) and on (1)
        command=relayB_slider_change,
        width=300
    )
    relayB_slider.set(0)  # Default to off
    relayB_slider.grid(row=3, column=1, padx=20, pady=20)

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
