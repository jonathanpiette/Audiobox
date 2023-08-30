import board
from adafruit_pn532.i2c import PN532_I2C

# Create an instance of the PN532 class using I2C
i2c = board.I2C()
pn532 = PN532_I2C(i2c)

# Initialize communication with the PN532
pn532.SAM_configuration()

while True:
    # Check if an NFC card is present
    uid = pn532.read_passive_target(timeout=0.5)

    if uid is not None:
        print("Found NFC card with UID:", [hex(i) for i in uid])
    else:
        print("No card detected.")
