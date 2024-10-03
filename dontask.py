import network
import urequests
import time
import machine

# Initialize the wlan interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to the Wi-Fi network
wlan.connect("Galaxy M327FC2", "notpaperplane47")

# Wait for the connection to be established
while not wlan.isconnected():
    time.sleep(1)

# Set the Firebase database URL and authentication token
firebase_url ="https://dontaskkk-default-rtdb.firebaseio.com/pico.json" #"https://dontask-b1a62-default-rtdb.firebaseio.com/pico.json"  # Notice the 'pico' path included here
auth_token = "AIzaSyBXUMpONE-73sLh3RsQU2lXfaJ8BjjHGa8"  #"qqgiXfuhfCP5fRsSqvfsJvsbSaOp2ZMCjC0SyMck"

# Set the sensor data key
sensor_key = "SwitchState"

# Set the time key
time_key = "Time"
count_key = "Count"
count_data = 0

# Initialize the GPIO pin for the switch (assuming Pin 14 is used)
switch_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    # Get the current time (using the time module)
    current_time = time.localtime()
    time_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(current_time[0], current_time[1], current_time[2], current_time[3], current_time[4], current_time[5])

    # Read the switch state (1 if on, 0 if off)
    switch_state = switch_pin.value()
    count_data += 1

    # Construct the URL for the Firebase database
    url = firebase_url + "?auth=" + auth_token

    # Create a dictionary to hold the switch state and time
    data = {
        count_key: count_data,
        time_key: time_str,
        sensor_key: "On" if switch_state == 1 else "Off"  # Store "On" or "Off" as the sensor data
    }

    print(data)

    try:
        # Use PATCH to update the data on Firebase
        response = urequests.patch(url, json=data, stream=True)  # Stream the response to avoid loading into memory

        # Check if the update operation was successful
        if response.status_code == 200:
            print("Data updated successfully")
        else:
            print("Error updating data")

        # Always close the response to free up memory
        response.close()

    except OSError as e:
        print("Error:", e)
        # Retry after 5 seconds
        time.sleep(5)
        continue

    # Wait for 15 seconds before checking again
    time.sleep(5)


