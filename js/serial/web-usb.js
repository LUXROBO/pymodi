/**
 * Cloud에 이용될 webUSB 라이브러리
 * @author June
 */
import { Port } from './port';

export const WebUSB = (() => {
  let instance;

  function init() {
    return {
      getPorts() {
        return navigator.usb.getDevices().then((devices) => {
          return devices.map((device) => new Port(device));
        });
      },

      requestPort() {
        const filters = [
          // LUXROBO MODI
          { vendorId: 0x2fde, productId: 0x0002 }
        ];

        return navigator.usb
          .requestDevice({ filters })
          .then((device) => new Port(device));
      }
    };
  }

  return {
    getInstance() {
      if (!instance) {
        instance = init();
      }

      return instance;
    }
  };
})();

export default WebUSB;
