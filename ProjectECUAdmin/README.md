![logo](images/HeadECU.png)

 
## About
Head ECU is one of the roles in [Project ECU](https://github.com/spitzc32/Project-ECU) that mainly acts as a server in a distributed server system. It is mainly focused on the Information and Volunteer Services side of the whole Community. It regulates the necessary level of cooperation and information needed to be passed incase an emergency request or an event needing a volunteer occurs. You can see them in the Home Panel in the announmcent Page when you use lil' ECU or if any notifications you receive has an update or announcement attached to it.       

## How it Works
There are two roles it mainly plays: one is an announcer for important events or happenings and two, is a host to cooperation of our lil' ECU's. Using OneSignal API, it distributes the information locally obtained to update the lil' ECUs of either an announcement or an update to the happenings around the community. The boundaries are then decided by [Geopy](https://geopy.readthedocs.io/en/stable/), a Python client for locating which users are going to be notified inside the domain set of the Head.           

![Pic1]()

### Who can use Head ECU?
This website is intended for the use of the head or someone in charge of the community that can deploy volunteers and frontliners that can help a person in need. The person who can use this website can be a head of an organization that sets out to help a particular area as long as it is nearby their vicinity. For establishments and partnered hospitals see the other folders in the source code and for individual users please use the application.

### Getting Started
Before proceeding please do the prerequisites in [Project ECU](https://github.com/spitzc32/Project-ECU). Those are the dependencies needed in order for this web application to work. Also do take note that each page has its specified purpose please read their usage in each of their source code before using it. This web application runs on local host port 5000. Make sure that any other service that uses this port are turned off. 

#### Running the Application
After doing the prerequisites in [Project ECU](https://github.com/spitzc32/Project-ECU), run the program in cmd with the following command. This instruction is for windows users only. 

```running
cd ProjectECUAdmin

python app.py
```

On the application, You will need to register as a Head Account. Please be notified that only a handful of users may sign in as the Head. If you are the head of an organization, see to it that there is only one centralized controller on your vicinity.









