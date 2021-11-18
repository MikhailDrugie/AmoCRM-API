# AmoCRM-API
## Done on Pycharm, using Django framework.
Before launching, edit ngrok.bat file and add your authtoken, so it can work properly.
Launching is performed by starting startapp.bat, it opens 2 windows (one - with ngrok, another - with django server).

At the first time, you should type your own parameters, such as your amocrm subdomain and widget's secret key and client id. Thereafter, you won't need to type them, as they will be stored in the static folder, and the only thing that setup.py will do is setting url that is provided by ngrok every time you launch the app.

You have to put the https url from setup.py (it can also be found in the ngrok window) in your widget (https://shueppsh987.amocrm.ru/settings/widgets/) and restart it then. You should do that before accessing to the url itself because after restarting, widget sends access code to the url, which is used to get *access token*.

The access token is the main part on which working with AmoCRM is based. After you recieve it, you can get contact list in /contacts/ (after updating it), post your own contacts and patch existing ones. Every posting and patching makes a phantom lead (with the price of zero) with the sent data.

I'm glad that I've finally deployed this project, as it shows the level of experience I have.
