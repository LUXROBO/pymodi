import modi
import time

if __name__ == "__main__":
    bundle = modi.MODI()
    lcd = bundle.displays[0]

    lcd.text("hi")
    time.sleep(2)
    lcd.variable(10.25, 1, 1)
    time.sleep(2)

    bundle.exit()
