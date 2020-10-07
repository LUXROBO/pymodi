import { WebUSB } from './web-usb';

export function connect() {
    const usb = WebUSB.getInstance();

    usb
      .requestPort()
      .then((selectedPort) => {
        const port = selectedPort;
        port.connect().then(
          (res) => {
            console.log(`Response: ${res}`);
          },
          (error) => {
            console.log(`Connection error: ${error}`);
          }
        );
      })
      .catch((error) => {
        console.log(`Connection error: ${error}`);
      });
  }
  
  export const disconnect = () => {
    const usb = WebUSB.getInstance();
    
    usb
      .getPorts()
      .then((selectedPorts) => {
        const ports = selectedPorts;
        ports.map((port) => port.disconnect());
      })
      .catch((error) => {
        console.log(`Connection error: ${error}`);
      });
  };
  
  export const setRGB = () => {
    const usb = WebUSB.getInstance();
    const textEncoder = new TextEncoder();
  
    const ledVal = document.getElementById('led-select').value;
    let codeStr = '';
  
    if (ledVal !== undefined) {
      codeStr = `{"c":4,"s":16,"d":1466,"b":"${ledVal}","l":8}`;
    } else {
      console.log('LED Colour not selected');
    }
  
    const onError = (error) => {
      console.log(`Error: ${error}`);
    };
  
    usb.getPorts().then((ports) => {
      if (ports !== undefined) {
        ports.map((port) => {
          return port.send(textEncoder.encode(codeStr)).catch(onError);
        });
      }
    });
  };
