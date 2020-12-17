History
==

0.1.0 (2018-06-28)
--
1. Release initial version of the package on in-house GitLab

0.1.1 (2018-07-20)
--
1. Fix requirements
2. Fix include path

0.1.2 (2018-07-23)
--
1. Python 3.4 support

0.2.0 (2018-07-25)
--
1. Implement Speaker module
2. Implement Display module

0.2.1 (2018-07-27)
--
1. Implement speaker module's tune() and off() methods
2. Remove duplicated codes

0.3.0 (2018-07-28)
--
1. Support python 2.7
2. Speed up the performance

0.3.1 (2018-07-28)
--
1. Fix requirements

0.4.0 (2018-08-20)
--
1. Improve performance
2. Complete first documentation

0.5.0 (2018-08-22)
--
1. Change the project name to pyMODI

0.5.1 (2018-11-07)
--
1. Fix "No MODI network module connected" issue

0.5.2 (2019-10-11)
--
1. Can control a pair of motors of the motor module by torque(), speed(),
   angle()

0.6.0 (2019-10-18)
--
1. Improve performance

0.7.0 (2020-01-23)
--
1. Implement individual motor control
2. Implement set variable method in display
3. Implement test cases for each modi modules
4. Implement multiprocessing version of pymodi
5. Bug fixes

0.7.1 (2020-02-07)
--
1. Refactor file structures
2. Bug fixes

0.8.0 (2020-05-07)
--
1. Implement Can Message Handler
2. Implement Topology Manager
3. Improve connection reliability by separating communication functions
4. Bug fixes

0.9.0 (2020-07-07)
--
1. Implement Module Firmware Updater
2. Implement bluetooth connection via SPP
3. Implement MODI Priority Queue to increase response speed
4. Implement PyMODI tutor for teaching new-comers
5. Support multi MODI network modules given appropriate COM ports
6. Refactor getter/setter for each MODI module
7. Refactor motor module to use set_motor_channel internally
8. Update property values when setting properties
9. Add usage/creation example to the repository
10. Bug fixes

1.0.0 (2020-09-15)
--
1. Implement Network Firmware Updater
2. Implement BLE connection (excluding macOS support)
3. Implement MODI Play support via network module
4. Refactor module getter/setter interface
5. Enhance topology manager to work with battery module
6. Add functionality to reset existing user code on the modules
7. Bug fixes

1.0.1 (2020-10-06)
--
1. Implement experimental BLE functionality on Windows and macOS
2. Improve BLE connection stability in Linux Platform
3. Implement module usage manual (i.e. quick-start)
4. Implement module inspection functionality (i.e. diagnose)
5.  Refactor GUI debugger design, fix initialization issue on macOS
1.1.0 (2020-12-17)
--
1. Implement GUI Firmware Updater in PyMODI
2. Implement network base (STM32) firmware updater
3. Implement GD32 firmware updater
4. Implement [VirtualMODI](https://github.com/luxrobo/virtual-modi) integration code

