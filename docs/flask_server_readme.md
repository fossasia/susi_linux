# Smart Speaker Server

This server will be automatically added to auto boot from the `wap.sh` script and will be removed from the auto boot list when the `rwap.sh` script is executed.
<br>
This server can be access on port 5000 when on the same network and `http:10.0.0.1:5000` when on raspi access point
<br>
## Tech Stack
* Flask is used for the backend
* The front-end is a just an HTML file

## API Endpoints
* /
  * This Endpoint returns a basic HTML introductory page

* /wifi_credentials
   * Below are the parameters 
   * 'wifissid' is the SSID of the WIFI network you want to configure
   * 'wifipassd' is the PASSWORD of that WIFI network

* /config
   * The endpoint looks like /config?stt=google&tts=google&hotword=y&wake=n
   * 'stt' is the name of Speech To Text Service Provider
     - You can choose from 'google', 'ibm', 'bing', 'sphinx'
   * 'tts' is the name of Text To Speech Provider
     - You can choose from 'google', 'ibm', 'flite'
   * 'hotword' is the choice if you want to use Snowboy as the service for hotword prediction
     - You can choose from 'y' or 'n'
   * 'wake' is the choice if you want to use an external wake button
     - You can choose from 'y' or 'n'

* /auth/'choice'/'email'/'password'  
   * 'choice' is the choice if you want to use the speaker in the authenticated mode
     - You can choose from 'y' or 'n'
   * 'email' is the email of the user
   * 'password' is the corresponding password
	