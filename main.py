import asyncio
from bleak import BleakScanner, BleakClient

def get_read_write_input():
    user_input = input("Read (R/r) or Write (W/w) (Q/q to quit): ")
    if user_input.upper() == "R":
        return "R"
    elif user_input.upper() == "W":
        return "W"
    elif user_input.upper() == "Q":
        return None
    else:
        print("Invalid input, try again")
        return get_read_write_input()

def get_characteristic_input(characteristics):
    user_input = input("Select Characteristic (L/l to list, Q/q to quit): ")
    if user_input.upper() == "L":
        for x, char in enumerate(characteristics):
            print(str(x) + ": " + char.uuid, char.properties)
        return get_characteristic_input(characteristics)
    elif user_input.upper() == "Q":
        return None
    else:
        try:
            int_input = int(user_input)
            print("Selected: " + characteristics[int_input].uuid)
            return characteristics[int_input]
        except:
            print("Invalid input, try again:")
            return get_characteristic_input(characteristics)

def get_message_input():
    user_input = input("Enter Message (Q/q to quit): ")
    if user_input.upper() == "Q":
        return None
    else:
        return user_input


async def main():
    devices = await BleakScanner.discover(timeout=4)
    device_name = "ESP_GATTS_DEMO"
    device_found = False
    for d in devices:
        if d.name == device_name:
            device_found = True
            print(device_name + " detected\nName: " + d.name + "\nAddress: " + d.address + "\nDetails: " + str(d.details))
            address = d.address
            client = BleakClient(address)
            try:
                await client.connect()
                print("\nConnection to " + d.name + " successful")
                services = await client.get_services()
                characteristics = []
                print("Characteristics:")
                for x, char in enumerate(services.characteristics.values()):
                    characteristics.append(char)
                    print(str(x) + ": " + char.uuid, char.properties)
                print()

                stop = False
                while stop is False:
                    read_write_input = get_read_write_input()
                    if read_write_input is None:
                        stop = True
                        continue

                    characteristic_input = get_characteristic_input(characteristics)
                    if characteristic_input is None:
                        stop = True
                        continue

                    if read_write_input == "R":
                        message_received = await client.read_gatt_char(characteristic_input)
                        print("STRING: " + str(message_received)[12:-2])
                        hex_str = ""
                        for x in message_received:
                            hex_str += str(x).ljust(2, '0') + " "
                        print("BYTES :", hex_str)
                        print("DATA LENGTH:", len(message_received))
                    else:
                        message_input = get_message_input()
                        message_to_send = bytes(str.encode(str(message_input)))
                        await client.write_gatt_char(characteristic_input, message_to_send)

                        message_received = await client.read_gatt_char(characteristic_input)
                        if message_to_send == message_received:
                            print("Sent: " + message_input)
                        else:
                            print("Message failed to send")
            except Exception as e:
                print(e)
            finally:
                await client.disconnect()
    if device_found is False:
        print(device_name + " not found")
        print(str(len(devices)) + " devices found: ")
        for device in devices:
            print(device)


asyncio.run(main())
