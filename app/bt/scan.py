import time
import signal
import simplepyble
import sys
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)


#from registerDevice import trust_device

interrupted = False

def signal_handler(sig, frame):
    logging.info('You pressed Ctrl+C!')
    interrupted = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def log_peripheral(peripheral):
    connectable_str = "Connectable" if peripheral.is_connectable() else "Non-Connectable"
    logging.info(f"{peripheral.identifier()} [{peripheral.address()}] - {connectable_str}")
    logging.info(f'    Address Type: {peripheral.address_type()}')
    logging.info(f'    Tx Power: {peripheral.tx_power()} dBm')
    logging.info(f'    rssi: {peripheral.rssi()}')
    logging.info(f'    mtu: {peripheral.mtu()}')

    manufacturer_data = peripheral.manufacturer_data()
    for manufacturer_id, value in manufacturer_data.items():
        logging.info(f"    Manufacturer ID: {manufacturer_id}")
        logging.info(f"    Manufacturer data: {value}")

    services = peripheral.services()
    for service in services:
        logging.info(f"    Service UUID: {service.uuid()}")
        logging.info(f"    Service data: {service.data()}")

    try:
            services = peripheral.services()
            service_characteristic_pair = []
            for service in services:
                for characteristic in service.characteristics():
                    service_characteristic_pair.append((service.uuid(), characteristic.uuid()))

                # Query the user to pick a service/characteristic pair

                for i, (service_uuid, characteristic) in enumerate(service_characteristic_pair):
                    service_uuid, characteristic_uuid = service_characteristic_pair[i]
                    # Write the content to the characteristic
                    contents = peripheral.read(service_uuid, characteristic_uuid)
                    logging.info(f"Contents: {contents}")
    except:
        logging.info("Error getting services")

def connect(peripheral):
    if peripheral.is_connectable():
        logging.info(f"Connecting to: {peripheral.identifier()} [{peripheral.address()}]")
        peripheral.connect()
        #trust_device(peripheral.address())
    return
        
    
def scan_for_devices():
        global interrupted
        adapters = simplepyble.Adapter.get_adapters() # type: ignore

        if len(adapters) == 0:
            logging.info("No adapters found")
            
        choice=0

        adapter = adapters[choice]
        adapter.set_callback_on_scan_start(lambda: logging.info("Scan started."))

        def scan_completed():
            logging.info("Scan complete.")
            global interrupted
            interrupted = True
            
        adapter.set_callback_on_scan_stop(scan_completed)


        def scan_found(peripheral):
            logging.info(f"Found {peripheral.identifier()} [{peripheral.address()}] connectable:{peripheral.is_connectable()}")
            if peripheral.address() == "[B0:F0:0C:0D:FD:28]":
                logging.info("FOUND SOUNDCORE HEADPHONES [B0:F0:0C:0D:FD:28]")
            if peripheral.address() == "B0:F0:0C:0D:FD:28":
                logging.info("FOUND SOUNDCORE HEADPHONES B0:F0:0C:0D:FD:28")
                logging.info(peripheral.is_connectable())
            else:
                logging.info(peripheral.address())
            
            if  peripheral.is_connectable() and peripheral.address() == "B0:F0:0C:0D:FD:28":
                logging.info(f"Connecting to {peripheral.address()}")
                connect(peripheral)
                time.sleep(5)
                global interrupted
                interrupted = True

        adapter.set_callback_on_scan_found(scan_found)
        
        def scan():
            adapter.scan_for(10000)
            while not interrupted:
                time.sleep(0.2)
            return
        scan_thread = threading.Thread(target=scan)
        scan_thread.start()
        scan_thread.join()

