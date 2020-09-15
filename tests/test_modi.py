# import unittest
#
# from unittest import mock
#
# from modi.modi import MODI
#
# from modi.module.setup_module.setup_module import SetupModule
# from modi.module.input_module.input_module import InputModule
# from modi.module.output_module.output_module import OutputModule
#
# from modi.module.input_module.button import Button
# from modi.module.input_module.dial import Dial
# from modi.module.input_module.env import Env
# from modi.module.input_module.gyro import Gyro
# from modi.module.input_module.ir import Ir
# from modi.module.input_module.mic import Mic
# from modi.module.input_module.ultrasonic import Ultrasonic
#
# from modi.module.output_module.display import Display
# from modi.module.output_module.led import Led
# from modi.module.output_module.motor import Motor
# from modi.module.output_module.speaker import Speaker
#
# from modi.util.misc import module_list
#
#
# class TestModi(unittest.TestCase):
#     """Tests for 'modi' class."""
#
#     def setUp(self):
#         """Set up test fixtures, if any."""
#         mock_input_values = (-1, -1, None)
#         mock_modules = [
#             SetupModule(*mock_input_values),
#             InputModule(*mock_input_values),
#             OutputModule(*mock_input_values),
#
#             Button(*mock_input_values),
#             Dial(*mock_input_values),
#             Env(*mock_input_values),
#             Gyro(*mock_input_values),
#             Ir(*mock_input_values),
#             Mic(*mock_input_values),
#             Ultrasonic(*mock_input_values),
#
#             Display(*mock_input_values),
#             Led(*mock_input_values),
#             Motor(*mock_input_values),
#             Speaker(*mock_input_values),
#         ]
#
#         self.modi = MODI()
#
#         self.modi._ser_proc = mock.Mock()
#         self.modi._exe_thrd = mock.Mock()
#         self.modi._modules = mock_modules
#
#     def tearDown(self):
#         """Tear down test fixtures, if any."""
#         del self.modi
#
#     def test_get_modules(self):
#         """Test modules getter method."""
#         actual_modules = self.modi.modules
#         self.assertIsInstance(actual_modules, module_list)
#         expected_modules = module_list(
#             self.modi.modules
#         )
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_buttons(self):
#         """Test buttons getter method."""
#         actual_modules = self.modi.buttons
#         expected_modules = module_list(
#             self.modi.modules, 'button'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_dials(self):
#         """Test dials getter method."""
#         actual_modules = self.modi.dials
#         expected_modules = module_list(
#             self.modi.modules, 'dial'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_envs(self):
#         """Test envs getter method."""
#         actual_modules = self.modi.envs
#         expected_modules = module_list(
#             self.modi.modules, 'env'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_gyros(self):
#         """Test gyros getter method."""
#         actual_modules = self.modi.gyros
#         expected_modules = module_list(
#             self.modi.modules, 'gyro'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_irs(self):
#         """Test irs getter method."""
#         actual_modules = self.modi.irs
#         expected_modules = module_list(
#             self.modi.modules, 'ir'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_mics(self):
#         """Test mics getter method."""
#         actual_modules = self.modi.mics
#         expected_modules = module_list(
#             self.modi.modules, 'mic'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_ultrasonics(self):
#         """Test ultrasonics getter method."""
#         actual_modules = self.modi.ultrasonics
#         expected_modules = module_list(
#             self.modi.modules, 'ultrasonic'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_displays(self):
#         """Test displays getter method."""
#         actual_modules = self.modi.displays
#         expected_modules = module_list(
#             self.modi.modules, 'display'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_leds(self):
#         """Test leds getter method."""
#         actual_modules = self.modi.leds
#         expected_modules = module_list(
#             self.modi.modules, 'led'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_motors(self):
#         """Test motors getter method."""
#         actual_modules = self.modi.motors
#         expected_modules = module_list(
#             self.modi.modules, 'motor'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#     def test_get_speakers(self):
#         """Test speakers getter method."""
#         actual_modules = self.modi.speakers
#         expected_modules = module_list(
#             self.modi.modules, 'speaker'
#         )
#
#         self.assertIsInstance(actual_modules, module_list)
#         self.assertEqual(actual_modules, expected_modules)
#
#
# if __name__ == "__main__":
#     unittest.main()
