import modi

"""
Example script for the usage of env module
Make sure you connect 1 env module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI()
    env = bundle.envs[0]

    while True:
        print("humidity: {0:<10} temp: {1:<10} "
              "brightness: {2:<10} R: {3:<10}"
              "G: {4:<10} B: {5:<10}".format(env.humidity,
                                             env.temperature,
                                             env.brightness,
                                             env.red, env.green,
                                             env.blue), end='\r')
