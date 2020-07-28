![logo]()

 
## About
Head ECU is one of the roles in [Project ECU](https://github.com/spitzc32/Project-ECU) that mainly acts as a server in a distributed server system. It is mainly focused on the Information and Volunteer Services side of the whole Community. It regulates the necessary level of cooperation and information needed to be passed incase an emergency request or an event needing a volunteer occurs. You can see them in the Home Panel in the announmcent Page when you use lil' ECU or if any notifications you receive has an update or announcement attached to it.       

## How it Works
There are two roles it mainly plays: one is an announcer for important events or happenings and two, is a host to cooperation of our lil' ECU's. Using OneSignal API, it distributes the information locally obtained to update the lil' ECUs of either an announcement or an update to the happenings around the community. The boundaries are then decided by [Geopy](https://geopy.readthedocs.io/en/stable/), a Python client for locating which users are going to be notified inside the domain set of the Head.           

![Pic1]()

### DMS LITE
The DMS LITE is the open source version of the cloud DMS. DMS LITE gives you simple network activity and data visuals.

The PaPa Duck is running a different Firmware than the regular ClusterDuck Protocol PaPa example.

### Example of ClusterDuck Protocol Network

![](public/images/CDP-NETWORK-EXPLAIN.jpg)

### Local ClusterDuck Protocol Network

![](public/images/PAPI-EXPLAIN-3.jpg)

## Parts required

- Raspberry Pi (3B+ preffered)
   - for using a pi zero you need a different setup for node.js
- Micro SD-Card 16GB or more
  - Raspbian OS installed
- Mouse and Keyboard
- Monitor
- Wired Ethernet Connection

- Latest Copy of [ClusterDuck Protocol](https://github.com/Code-and-Response/ClusterDuck-Protocol)


# Setup 
## How To Install
The PaPi and DMS LITE both need some setup before you can start seeing your data. To turn the Raspberry Pi into the PaPi, you will need to install multiple modules. 

## Prepare Heltec or TTgo Board for PaPi
1. goto [PAPI DMS Lite Examples](https://github.com/Code-and-Response/ClusterDuck-Protocol/tree/master/examples/PaPi-DMS-Lite-Examples "DMS PAPI Examples")
2. Select which example you need based off of your particular install.
3. Upload the .INO and you are set to move on 

## Script Install 
Both Raspbian images have Python 2 preinstalled but Raspbian Lite does not have python 3 preinstalled. But you will need to set you Pi to use python 3 as default.

1. check your python version by running: python --version
  *** if you don't see python 3 continue on to 2.**
2. nano ~/.bashrc and add this to the very bottom alias python='/usr/bin/python3'

now try this again python --version you should see your default is python 3 now.

#### For Usb Serial 
1. Make sure you connect the LoRa board to the Raspberry Pi.
2. chmod u+x serial-install.sh will make the code excutable 
3. ./Serial-install.sh will make the code run 
4. sit back and kick up your feet because install will take a bit

The DMS Lite will automatically open in a full sized window.

#### After Install Run
The next time you boot the Pi CD into the DMS-LITE folder and run the following script.
1. chmod u+x run.sh
2. now that you made the script executable run it by typing ./run.sh
*** This will launch the scripts and bring you into kiosk mode. Which is full screen full resolution with no bars or anything. to exit out of this either reboot the pi or press fn f4 key to get back to desktop. ***

In your Browser go to Localhost:3000 to see the dms-lite

NOTE: *You need to run the two scripts in two separate terminals.*

#### For Wifi Acces Point 
1. chmod u+x Wifi-install.sh will make the code excutable 
2. ./Wifi-install.sh will make the code run 
3. sit back and kick up your feet because install will take a bit

NOTE: *You need an Internet Connection to install the packages and the DMS LITE application. After the Raspberry Pi is turned into an Access Point it doesn't have WiFi capabilities anymore and you will need a LAN connection for final setup.*

After you have installed the required dependencies you can the two scripts.

`python3 Wifi_sqlwriter.py`

`npm run start`

In your Browser go to Localhost:3000 to see the dms-lite

NOTE: *You need to run the two scripts in two separate terminals.*








![logo](public/images/footer.png)
