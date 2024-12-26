import Jetson.GPIO as GPIO
import socket
import logging
import time

class SmartLEDClient:
    def __init__(self, out_pins=[7, 12], in_pins=[11], host="localhost", port=5500):
        self.configure_logging()
        self.out_pins = out_pins
        self.in_pins = in_pins
        self.motion_detected = False
        self.last_motion_time = 0
        self.host, self.port = host, port
        self.setup_gpio()
        self.connect_to_server()

    def configure_logging(self):
        logging.basicConfig(
            filename="client.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info("Client initialized.")

    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        for pin in self.out_pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        for pin in self.in_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.add_event_detect(
                pin, GPIO.RISING, callback=self.motion_detected_callback, bouncetime=5000
            )
        logging.info(f"GPIO configured: Outputs={self.out_pins}, Inputs={self.in_pins}")

    def motion_detected_callback(self, channel):
        self.last_motion_time = time.time()
        if not self.motion_detected:
            self.motion_detected = True
            GPIO.output(self.out_pins[0], GPIO.HIGH)
            GPIO.output(self.out_pins[1], GPIO.LOW)
            self.server_conn.send(b"1")
            logging.info(f"Motion detected on pin {channel}. Light turned ON.")
        else:
            logging.info(f"Motion detected again on pin {channel}.")

    def no_motion_detected(self):
        if self.motion_detected and time.time() - self.last_motion_time > 5:
            self.motion_detected = False
            GPIO.output(self.out_pins[0], GPIO.LOW)
            GPIO.output(self.out_pins[1], GPIO.HIGH)
            self.server_conn.send(b"0")
            logging.info("No motion detected. Light turned OFF.")

    def connect_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            self.server_conn = client_socket
            logging.info(f"Connected to server at {self.host}:{self.port}")
            self.run()

    def run(self):
        while True:
            time.sleep(1)
            if not self.motion_detected:
                self.no_motion_detected()
            self.server_conn.send(b"2")
            server_response = self.server_conn.recv(1024)
            if server_response == b"2":
                break
        self.cleanup()

    def cleanup(self):
        GPIO.cleanup()
        self.server_conn.close()
        logging.info("GPIO cleaned up and client connection closed.")


if __name__ == "__main__":
    client = SmartLEDClient(port=5500)
