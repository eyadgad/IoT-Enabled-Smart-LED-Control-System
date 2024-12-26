# IoT-Enabled Smart LED Control System with Adafruit IO and Blynk Cloud

---

## Project Overview
This repository contains the implementation of a **Smart LED Control System** using IoT technologies. The project integrates **Adafruit IO**, **Blynk Cloud**, and **Jetson Nano GPIO** to control and monitor an LED remotely. It includes server-client communication for real-time updates and incorporates motion detection to automate LED operations.

### Key Features:
- Remote LED control using Adafruit IO and Blynk Cloud.
- Motion detection using Jetson Nano GPIO.
- Server-client communication via Python socket programming.
- Logging for debugging and monitoring.
- Modular and extensible design for future enhancements.

---

## Repository Structure
The repository includes the following files:

- **`server.py`**: Implements the server-side logic to handle Adafruit IO and Blynk Cloud communication and manage client requests.
- **`client.py`**: Implements the client-side logic to interact with Jetson Nano GPIO for motion detection and communicate with the server.
- **`requirements.txt`**: Contains the Python dependencies required for the project.
- **`README.md`**: Documentation for setup and usage.

---

## Prerequisites
1. **Hardware**:
   - Jetson Nano (or Raspberry Pi as an alternative).
   - LEDs, motion sensor (PIR), and necessary jumper wires.

2. **Accounts**:
   - Adafruit IO account ([Sign up here](https://io.adafruit.com/)).
   - Blynk Cloud account ([Sign up here](https://blynk.io/)).

3. **Software**:
   - Python 3.8 or higher.
   - Libraries listed in `requirements.txt`.

---

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/eyadgad/IoT-Enabled-Smart-LED-Control-System.git
   cd IoT-Enabled-Smart-LED-Control-System
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up GPIO permissions for Jetson Nano:
   ```bash
   sudo groupadd -f gpio
   sudo usermod -a -G gpio $USER
   newgrp gpio
   ```

---

## Configuration
1. **Adafruit IO Setup**:
   - Create an Adafruit IO account.
   - Create feeds:
     1. `led_status`
     2. `button_status`
   - Generate your Adafruit IO Key and Username.

2. **Blynk Cloud Setup**:
   - Create a new device in the Blynk app.
   - Add a virtual pin `V0` for LED control.
   - Add a virtual pin `V1` for button status.
   - Generate your Blynk Auth Token.

3. **Update the Code**:
   - Open `server.py` and update the following variables in the `initialize_adafruit_io` function:
     ```python
     adafruit_key = "YOUR_ADAFRUIT_IO_KEY"
     adafruit_user = "YOUR_ADAFRUIT_USERNAME"
     ```
   - Update the Blynk token:
     ```python
     token = "YOUR_BLYNK_TOKEN"
     ```

---

## Usage
Follow these steps to set up and run the system:

### Step 1: Start the Server
1. Open a terminal on your Jetson Nano or server system.
2. Run the server:
   ```bash
   python server.py
   ```

### Step 2: Configure the Client
1. Ensure the client device (Jetson Nano or Raspberry Pi) is connected to the same network as the server.
2. Update the `client.py` file:
   - Replace the host with your server's IP address:
     ```python
     host = "SERVER_IP_ADDRESS"
     port = 5500
     ```

### Step 3: Connect the Hardware
1. Connect LEDs to the GPIO pins specified in the `client.py` file (default: pins 7 and 12).
2. Connect the motion sensor to the GPIO pin specified (default: pin 11).

### Step 4: Run the Client
1. Open a terminal on the client device.
2. Run the client:
   ```bash
   python client.py
   ```

### Step 5: Test the System
1. Trigger the motion sensor to turn on the LED.
2. Observe the real-time updates on Adafruit IO and Blynk Cloud dashboards.
3. Use the Blynk app to manually control the LED.

---

## Example Workflow
1. **Motion Detected**:
   - Motion sensor sends a signal to the client.
   - Client turns on the LED and notifies the server.
   - Server updates the Adafruit IO and Blynk Cloud dashboards.

2. **Manual Control**:
   - Use the Blynk app to toggle the LED.
   - Server updates the Adafruit IO feed.

---

## Logs and Debugging
- **Server Logs**:
  - Stored in `server.log`.
  - Contains details of Adafruit IO and client communication.

- **Client Logs**:
  - Stored in `client.log`.
  - Contains details of GPIO events and server communication.

---

## Contact
For any questions or issues, contact **Eyad Gad** at [egad@uwo.ca](mailto:egad@uwo.ca).
