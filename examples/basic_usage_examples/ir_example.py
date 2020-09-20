import modi

"""
Example script for the usage of ir module
Make sure you connect 1 ir module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI()
    ir = bundle.irs[0]

    while True:
        print("{0:<10}".format(ir.proximity), end='\r')
