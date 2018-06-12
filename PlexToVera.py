import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as etree
import time
import configparser
import logging
import json

#Load configuration file
config = configparser.ConfigParser()
config.sections()
config.read('./PlexToVera.conf')

# Set up logging
LogLevel = int(config['GENERAL']['LogLevel'])
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filemode='w', filename='./log/PlexToVera.log', level=LogLevel)

# General Variables
DelayTime = int(config['GENERAL']['DelayTime'])
LightStatus = "ON"

# Plex Variables            
PlexServerIP = config['PLEX']['PlexServerIP']
PlexServerPort = config['PLEX']['PlexServerPort']
PlexServerToken = config['PLEX']['PlexServerToken']
PlexServerURL = 'http://' + PlexServerIP + ':' + PlexServerPort + '/status/sessions?X-Plex-Token=' + PlexServerToken
PlexClient = config['PLEX']['PlexClient']

#Vera Variables
VeraServerIP = config['VERA']['VeraServerIP']
VeraServerPort = config['VERA']['VeraServerPort']
VeraMovieLightingSceneID = config['VERA']['PlexMovieOnSceneID']
VeraBrightLightingSceneID = config['VERA']['PlexMovieOffSceneID']
VeraPausedLightingSceneID = config['VERA']['PlexMoviePauseSceneID']
VeraDayNightPlugidID = config['VERA']['DayNightPluginID']

#Set URL requests
DayNightStatusURL = 'http://' + VeraServerIP + ':' + VeraServerPort + '/data_request?id=status&output_format=json&DeviceNum=' + VeraDayNightPlugidID
TurnOnMovieLightingModeURL = 'http://' + VeraServerIP + ':' + VeraServerPort + '/data_request?id=lu_action&output_format=json&serviceId=urn:micasaverde-com:serviceId:HomeAutomationGateway1&action=RunScene&SceneNum=' + VeraMovieLightingSceneID
TurnOnBrightLightingModeURL = 'http://' + VeraServerIP + ':' + VeraServerPort + '/data_request?id=lu_action&output_format=json&serviceId=urn:micasaverde-com:serviceId:HomeAutomationGateway1&action=RunScene&SceneNum=' + VeraBrightLightingSceneID
TurnOnMidLightingModeURL = 'http://' + VeraServerIP + ':' + VeraServerPort + '/data_request?id=lu_action&output_format=json&serviceId=urn:micasaverde-com:serviceId:HomeAutomationGateway1&action=RunScene&SceneNum=' + VeraPausedLightingSceneID

#General Vera request function
def veraRequest(URL):
    response = urllib.request.urlopen(URL)
    content = response.read()
    data = json.loads(content.decode("utf8"))

    return data

#Request day or night status function
def veraDayNight(URL):

    DayNightDevice = 'Device_Num_' + VeraDayNightPlugidID
    data = veraRequest(URL)
    dayNightStatus = (data[DayNightDevice]['states'][0]['value'])

    return dayNightStatus

#Run scene execution on Vera function
def veraScene(URL):
    data = veraRequest(URL)
    VeraStatus = (data['u:RunSceneResponse']['OK'])

    if VeraStatus == "OK":
        logging.info('Command successfully sent')
    else:
             logging.info('Command Failed: Try %s of 5 : %s', x+1, RestURL)
             time.sleep(1)

#---------------------------
# Open the Status_sessions.xml from the Plex Server
# Read the xml file looking for our desired Plex Client
# Print Status

logging.info('============================================')
logging.info('--------------------------------------------')
logging.info('Starting PlexToVera Script')
logging.info('--------------------------------------------')
logging.info('Plex Server : %s', PlexServerURL)
logging.info('Plex Client : %s', PlexClient)
logging.info('VERA Server : http://%s:%s', VeraServerIP, VeraServerPort)
logging.info('--------------------------------------------')

print('--------------------------------------------')
print('Starting PlexToVera Script')
print('No further output here. See logfile for more details.')
print('Press Ctrl-C to Stop Program')
print('--------------------------------------------')

#Main
while True:
     logging.debug('-----------------------------------------')
     try:
         u = urllib.request.urlopen(PlexServerURL)
         tree = etree.parse(u)
         root = tree.getroot()
         try:
             value = root.find(".//*[@machineIdentifier='" + PlexClient + "']")
             MovieStatus = value.attrib["state"]
         except AttributeError:
             MovieStatus = "stopped"
         logging.debug('Movie is %s', MovieStatus)

         #Determine if night, if not it will skip light controls
         if veraDayNight(DayNightStatusURL) == '0':
             if MovieStatus == "playing":
                 if (LightStatus == "ON") or (LightStatus =="DIM"):
                     logging.info('Turning LIGHTS DOWN')
                     veraScene(TurnOnMovieLightingModeURL)
                     LightStatus = "OFF"
             elif MovieStatus == "paused":
                 if LightStatus == "OFF":
                     logging.info('Turning LIGHTS DIM')
                     veraScene(TurnOnMidLightingModeURL)
                     LightStatus = "DIM"
             else:
                 if (LightStatus == "OFF") or (LightStatus =="DIM"):
                     logging.info('Turning Lights UP')
                     veraScene(TurnOnBrightLightingModeURL)
                     LightStatus = "ON"

         logging.debug('Waiting for next polling interval.')
         time.sleep(DelayTime)
     except urllib.error.URLError as e:
             print(e.reason)
             print ('Plex Server Not Responding... waiting 1 minute.')
             time.sleep(60)
