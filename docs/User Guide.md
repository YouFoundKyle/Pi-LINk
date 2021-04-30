# Pi-LINk User Documentation
### Initial Setup
  1. SSH into your Raspberry Pi. Ensure you have sudo privileges with the user you are signed in as.
  2. Run the following command **(make sure you copy the entire command)**:  
  ```wget -O install_basic.sh https://raw.githubusercontent.com/YouFoundKyle/Pi-LINk/main/bin/install_basic.sh && chmod +x install_basic.sh && sudo bash install_basic.sh```
  3. Ensure the Ansible playbooks run to completion with no failures.
  4. Your Pi-LINk should now be set up. Check to see if the Pi-LINk Portal is live by going to your Raspberry Pi’s IP address and ```port 8080``` in a web browser.
  For example, if your Pi’s IP is ```192.1.1.1``` just type ```192.1.1.1:8080``` into the url bar. You do not need to create an account at this point, but you can if you want to.
  
### Linking IoT Devices
  1. Log into your local Home Assistant instance hosted on the Pi. Go to your Raspberry Pi’s IP address and ```port 8123``` in a web browser.
  For example, if your Pi’s IP is ```192.1.1.1``` just type ```192.1.1.1:8123``` into the url bar.  
  2. Create your local Home Assistant account when prompted by the onboarding screen.
  3. Go to Settings -> Integrations -> Local Tuya
  4. Follow the directions from [this guide](https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md) to setup your devices.

### Using the Pi-LINk Web Portal
  1. To access the Pi-LINk Portal, go to your Raspberry Pi’s IP address and ```port 8080``` in a web browser.
  For example, if your Pi’s IP is ```192.1.1.1``` just type ```192.1.1.1:8080``` into the url bar.
  2. Create your account if you have not already.
  3. Start exploring your network and data!
