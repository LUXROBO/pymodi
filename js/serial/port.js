export class Port {
    constructor(device) {
      this.device = device;
      this.interfaceNumber = 1;
      this.endpointIn = 1;
      this.endpointOut = 3;
    }
  
    connect() {
      const readLoop = () => {
        this.device.transferIn(this.endpointIn, 64).then(
          (result) => {
            console.log(result);
            readLoop();
          },
          (error) => {
            console.log(error);
          }
        );
      };
    
      return this.device
        .open()
        .then(() => {
          if (this.device.configuration === null) {
            console.log(this.device.selectConfiguration(1));
          }
        })
        .then(() => {
          const configurationInterfaces = this.device.configuration.interfaces;
          configurationInterfaces.forEach((element) => {
            element.alternates.forEach((elementalt) => {
              if (elementalt.interfaceClass === 0xff) {
                this.interfaceNumber = element.interfaceNumber;
                elementalt.endpoints.forEach((elementendpoint) => {
                  if (elementendpoint.direction === 'out') {
                    this.endpointOut = elementendpoint.endpointNumber;
                  }
                  if (elementendpoint.direction === 'in') {
                    this.endpointIn = elementendpoint.endpointNumber;
                  }
                });
              }
            });
          });
        })
        .then(() => this.device.claimInterface(this.interfaceNumber))
        .then(() => this.device.selectAlternateInterface(this.interfaceNumber, 0))
        .then(() =>
          this.device.controlTransferOut({
            requestType: 'class',
            recipient: 'interface',
            request: 0x22,
            value: 0x01,
            index: this.interfaceNumber
          })
        )
        .then(() => {
          readLoop();
        });
    }
  
    disconnect() {
      return this.device
      .controlTransferOut({
        requestType: 'class',
        recipient: 'interface',
        request: 0x22,
        value: 0x00,
        index: this.interfaceNumber
      })
      .then(() => this.device.close());
    }
  
    send(data) {
      return this.device.transferOut(this.endpointOut, data);
    }
  }
  
  export default Port;
  