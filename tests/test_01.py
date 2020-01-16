import modi
import time


if __name__ == "__main__":
        
    print('Program Start')
    bundle = modi.MODI()
    # button1 = bundle.buttons[0]
    # button2 = bundle.buttons[1]
    for _ in range(100):
        # print('main : ',bundle._modules, bundle._ids)
        time.sleep(0.1)
    time.sleep(20)

    print('Program End')