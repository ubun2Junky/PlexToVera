PlexToVera

First of all, I just want to give credit where credit is due.  Thanks to bsmith993 original PlexToInstean design, I was able to redesign his original app so it would work the Vera.  I am by no means a developer by any stretch of the imagination, so if anyone find a better alternative or code corrections, I'm always open to suggestions.  

Small, standalone Python script that monitors a Plex Server to determine if a specific Plex Client is playing a movie, and will turn Vera controlled lights up or down based on playback status.

GOAL

When you start watching a movie, dim your Zwave lights to a movie scene you have created. When you pause or stop the movie, return the movie lighting to a normal lighting mode.

REQUIREMENTS

- Plex Media Server
- Plex Client
- Vera contolled lighting, with a movie mode scene,  a NON movie mode scene and a paused movie scene. Movie mode intended to be off, non movie mode intended to be bright and paused mode intended to be dimmed.

INSTALLATION

- You must have Python installed. (Google it if you need help) This is written for Python 3.4 
- There is no installation for the script itself. Simply place the files in the following folder /opt/PlexToVera and then schedule a job using cron (or however else you'd like to trigger it). 
- Make a copy of the PlexToVera.conf.default file and rename it PlexToVera.conf and modify the file to your variables and fire up the script.
- Add this line to run as a cron "* * * * *  bash /opt/PlexToVera/checkScriptStatus.sh"
- The script will continuously run. It is low memory and CPU usage.

USAGE

Here's the plan... read the xml file from the Plex Server to see if a user defined Plex Home Theater Client is playing a movie. If it is and it's night time, set the lights to movie mode. When it pauses it dims the lights or if it stops, bring em up.
