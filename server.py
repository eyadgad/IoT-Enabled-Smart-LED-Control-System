import logging
import socket
import time
import requests
from Adafruit_IO import Client, Feed, RequestError

class SmartLEDServer:
    def __init__(self, host="localhost", port=5500):
        self.configure_logging()
        self.adafruit_io, self.feeds = self.initialize_adafruit_io()
        self.host, self.port = host, port
        self.token = "YOUR_BLYNK_TOKEN"  # Replace with your Blynk token
        self.start_server()

    def configure_logging(self):
        logging.basicConfig(
            filename="server.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logging.info("Server initialized.")

    def initialize_adafruit_io(
        self,
        adafruit_key = "YOUR_ADAFRUIT_IO_KEY",
        adafruit_user = "YOUR_ADAFRUIT_USERNAME",
        feed_names=["led_status", "button_status"],
        initial_values=[0, 1],
    ):
        logging.info("Connecting to Adafruit IO...")
        aio = Client(adafruit_user, adafruit_key)
        try:
            feeds = [aio.feeds(feed) for feed in feed_names]
        except RequestError:
            feeds = [aio.create_feed(Feed(name=feed)) for feed in feed_names]
        for feed, value in zip(feeds, initial_values):
            aio.send(feed.key, value)
        logging.info(f"Connected to Adafruit IO with feeds: {feed_names}")
        return aio, feeds

    def write_data(self, value, pin):
        self.adafruit_io.send(self.feeds[0].key, value)
        requests.get(
            f"https://blynk.cloud/external/api/update?token={self.token}&{pin}={value}"
        )
        logging.info(f"Data written: {value} to pin {pin}")

    def read_data(self, pin):
        blynk_response = requests.get(
            f"https://blynk.cloud/external/api/get?token={self.token}&{pin}"
        ).text
        if blynk_response == "0":
            return blynk_response
        adafruit_response = self.adafruit_io.receive(self.feeds[1].key).value
        return adafruit_response

    def handle_client(self, conn):
        while True:
            time.sleep(1)
            msg = conn.recv(1024)
            logging.info(f"Received message: {msg}")
            if msg == b"1":
                self.write_data(1, "v0")
            elif msg == b"0":
                self.write_data(0, "v0")
            elif msg == b"2":
                if self.read_data("v1") == "0":
                    conn.send(b"2")
                    break
                else:
                    conn.send(b"0")

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logging.info(f"Server listening on {self.port}")
            print("Waiting for connections...")
            conn, addr = server_socket.accept()
            logging.info(f"Connection accepted from {addr}")
            with conn:
                self.handle_client(conn)

    def close(self):
        logging.info("Server shutting down.")
        print("Server closed.")


if __name__ == "__main__":
    server = SmartLEDServer(port=5500)
