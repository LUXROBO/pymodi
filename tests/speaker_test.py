import modi
import time


if __name__ == "__main__":
    bundle = modi.MODI()
    spk = bundle.speakers[0]

    for i in range(100):
        k = i * 1.0
        spk.tune(k * 10.0, 50.0)
        print("freq : ", k)
        time.sleep(0.1)

    bundle.exit()
