__author__ = 'Callum'
# -*- coding: utf-8 -*-
#Python 3.7.3
#pax-slack.py - Notify Slack users of new Library items
#Version: 0.1
#Date: June 26th 2019
################ USAGE OF THE  PROGRAM #####################################
# Short Description:
# When a library item is tagged in Paxata with "Slack", notify the user

import requests, sys, os, json, string, copy, sched, time, shutil
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from requests.auth import HTTPBasicAuth

# (2) Get all of the datasources from Paxata that are tagged with "tag"
def get_tagged_library_items(auth_token,paxata_url,tag):
    tagged_datasets = []
    get_tags_request = (paxata_url + "/rest/library/tags")
    get_tags_response = requests.get(get_tags_request, auth=auth_token, verify=False)
    if (get_tags_response.ok):
        AllTagsDatasetsJson = json.loads(get_tags_response.content)
        i=0
        number_of_datasets = len(AllTagsDatasetsJson)
        while i < number_of_datasets:
            if (AllTagsDatasetsJson[i].get('name') == tag):
                tagged_datasets.append(AllTagsDatasetsJson[i].get('dataFileId'))
            i += 1
    else:
        print ("bad request> " + str(get_tags_response.status_code))
    return tagged_datasets

def post_message_to_slack(message):
    slack_url = "https://hooks.slack.com/services/"
    slack_unique_id = "T3Z1R3DNG/BKYDSEV3Q/8kai7rKDmM5Z7dJkW3FdfGtk"
    slack_message = '{"text": \"'+ message +'\"}'

    slack_request = slack_url + slack_unique_id
    try:
        slack_post_msg_response = requests.post(slack_request, verify=False, data=slack_message)
    except:
        print ("DEBUG: Posting message failed")

# get the Name of a Library from it's DatasetID
def get_name_of_datasource(auth_token,paxata_url,libraryId):
    url_request = (paxata_url + "/rest/library/data/"+str(libraryId))
    my_response = requests.get(url_request,auth=auth_token , verify=False)
    if(my_response.ok):
        jDataDataSources = json.loads(my_response.content)
        libraryName = jDataDataSources[0].get('name')
    return libraryName


def main():
    paxata_token = "fbf4f53e82544f3c9dfdbb0aa3337965"
    paxata_url = "https://dataprep.paxata.com"
    tag = "Slack"
    auth_token = HTTPBasicAuth("",paxata_token)    
    tagged_datasets = get_tagged_library_items(auth_token,paxata_url,tag)

    for libraryId in tagged_datasets:
        
        dataset_name = get_name_of_datasource(auth_token,paxata_url,libraryId)
        print ("datasset = " + dataset_name)
        post_message_to_slack(dataset_name + " awaiting your perusal. Run a profile? Click here ->")

if __name__ == '__main__':
    main()