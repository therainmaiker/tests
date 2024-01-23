from flask import Flask, request, jsonify
import binascii
import struct
from datetime import datetime

app = Flask(__name__)

def unpack(fmt, data):
    try:
        return struct.unpack(fmt, data)
    except struct.error:
        flen = struct.calcsize(fmt.replace('*', ''))
        alen = len(data)
        return f"Error: Expected {flen} bytes, but received {alen} bytes"

@app.route('/', methods=['POST'])
def handle_gps_data():
    try:
        data = request.data
        print(f"Received data: {binascii.hexlify(data)}")

        imei, gps_data = parse_teltonika_data(data)

        # Process and store data as needed (for example, print to console)
        print(f"IMEI: {imei}")
        print(f"GPS Data: {gps_data}")

        return jsonify({"status": "OK"})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

def parse_teltonika_data(data):
    hex_data = binascii.hexlify(data).decode('utf-8')
    imei = hex_data[4:16]

    if len(data) < 10:  # Adjust the length based on the actual expected size
        raise ValueError("Error: Invalid data length")

    gps_data = unpack("IHBB", data[20:30])  # Adjust the format based on your Teltonika protocol and expected size

    return imei, gps_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
