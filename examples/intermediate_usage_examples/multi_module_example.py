import modi

"""
This example explains the convention that pymodi uses when multiple modules
with the same type are connected.

When multiple modules are connected, the modules are sorted in ascending order
based on the position relative to the network module.

1. Distance from the network module
2. Left to Right
3. Top to Bottom
"""
if __name__ == "__main__":
    bundle = modi.MODI()
    led1 = bundle.leds[0]
    led2 = bundle.leds[1]
    bundle.print_topology_map(print_id=True)

"""
Case 1:
                       <<MODI Topology Map>>
======================================
   Network:67        Dial:2821       Button:2766       Led:1600
    Led:3712

In this case, since Led:3712 is closer to the network module,
led1 is Led:3712 and led2 is Led:1600


Case 2:
               <<MODI Topology Map>>
============================
    Led:3712        Button:2766       Led:1600
                     Network:67

In this case, two led modules are equidistant from the network module.
Therefore, we move on to Rule 2: Left to Right. Since Led:3712 is on the
left side, Led:3712 is led1 and Led:1600 is led2

Case 3:
      <<MODI Topology Map>>
=====================================
                      Led:3712
   Network:67       Button:2766
                       Led:1600

In this case, two leds are equidistant and also on the same column.
0In this case, since Rule 1 and 2 cannot distinguish two leds, we move to
Rule 3: Top to Bottom. Since Led:3712 is located higher than Led:1600,
Led:3712 is led1 and Led:1600 is led2.

Case4:
               <<MODI Topology Map>>
===================================================
                    Button:2766       Led:1600
                    Network:67
    Led:3712         Dial:2821

In this case, even though Led:1600 is located higher than Led:3712,
the rules have priorities. By Rule 2, Led:3712 becomes led1. Led:3712 is
led1 and Led:1600 is led2.
"""

"""
It is also possible to access modules by there id

led1 = bundle.leds.get(3712)
led2 = bundle.leds.get(1600)

Check the ids of the module by printing their topology map
"""
