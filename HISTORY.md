History
=======

0.1.0 (2018-06-28)
------------------
-   First release on in-house GitLab

0.1.1 (2018-07-20)
------------------
-   Requirements fix
-   Packages\' include path fix

0.1.2 (2018-07-23)
------------------
-   Python 3.4 support

0.2.0 (2018-07-25)
------------------
-   Speaker module support
-   Display module support

0.2.1 (2018-07-27)
------------------
-   Add speaker module\'s tune() and off() methods
-   Remove duplicated codes

0.3.0 (2018-07-28)
------------------
-   Support python 2.7
-   Speed up the performance

0.3.1 (2018-07-28)
------------------
-   Requirements fix

0.4.0 (2018-08-20)
------------------
-   Performance improvement
-   The first documentation complete

0.5.0 (2018-08-22)
------------------
-   Change the project name to pyMODI

0.5.1 (2018-11-07)
------------------
-   Fix \#26 (No MODI network module connected) issue

0.5.2 (2019-10-11)
------------------
-   Can control a pair of motors of the motor module by torque(),
    speed(), angle()

0.6.0 (2019-10-18)
------------------
-   Performance improvement
-   Bug fixes

0.7.0 (2020-01-23)
------------------
-   Implement individual motor control
-   Implement set variable method in display
-   Implement test cases for each modi modules
-   Implement multiprocessing version of pymodi
-   Bug fixes

0.7.1 (2020-02-07)
------------------
-   Refactor file structures
-   Bug fixes

0.8.0 (2020-05-07)
------------------
-   Implement Can Message Handler
-   Implement Topology Manager
-   Improve connection reliability by separating communication functions
-   Bug fixes

0.9.0 (2020-07-07)
------------------
-   Implement Module Firmware Updater
-   Implement bluetooth connection via SPP
-   Implement MODI Priority Queue to increase response speed
-   Implement PyMODI tutor for teaching new-comers
-   Support multi MODI network modules given appropriate COM ports
-   Refactor getter/setter for each MODI module
-   Refactor motor module to use set_motor_channel internally
-   Update property values when setting properties
-   Add usage/creation example to the repository
-   Bug fixes

1.0.0 (2020-09-15)
------------------
-   Implement Network Firmware Updater
-   Implement BLE connection (excluding macOS support)
-   Implement MODI Play support via network module
-   Refactor module getter/setter interface
-   Enhance topology manager to work with battery module
-   Add functionality to reset existing user code on the modules
-   Bug fixes
