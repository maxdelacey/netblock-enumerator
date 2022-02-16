#!/usr/bin/env python3

import sys
import json
import csv
import pandas as pd
import requests
import argparse
from requests.api import get
from datetime import datetime
from tabulate import tabulate


# api-endpoint
URL = "https://ip-netblocks.whoisxmlapi.com/api/v2"

# add your API key here (free from https://ip-netblocks.whoisxmlapi.com/api/signup)
key = ''


parser = argparse.ArgumentParser(
    description='Queries WhoisXMLAPI with the specified organisation name and returns all associated netblocks.')

parser.add_argument(
    "-n",
    required=True,
    dest="org",
    help="Name of organisation to query.")

parser.add_argument(
    "-oC",
    dest="out_csv",
    action="store_true",
    help="Ouput results to CSV in current directory. No need to specify filename.")

parser.add_argument(
    "-oJ",
    dest="out_json",
    action="store_true",
    help="Ouput full results to JSON in current directory. No need to specify filename.")

args = parser.parse_args()


def get_netblocks():
    
    if key == '':
        print("[!] No API key set. You need a WhoisXMLAPI key from https://ip-netblocks.whoisxmlapi.com/, it's free and allows for 1000 requests a month.")
        sys.exit(-1)
    else:
        try:
            PARAMS = {'apiKey':key,'org':args.org}
            r = requests.get(url = URL, params = PARAMS)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    try:
        data = r.json()
    except json.decoder.JSONDecodeError as err:
        print("No JSON in response. Error message:" + '\n' + err)
    return data


def create_filename():
    #create the filename variable, stripping whitespace and appending current date to the org name
    if ' ' in args.org:
        orgname = args.org.replace(" ","_")
    else:
        orgname = args.org
    dateTimeObj = datetime.now()
    dateObj = dateTimeObj.date()
    dateStr = dateObj.strftime("%d-%m-%Y")
    if args.out_csv:
        filetype = '.csv'
    if args.out_json:
        filetype = '.json'
    filename = orgname + "_" + "netblocks_" + dateStr + filetype
    return filename


def output_to_json():
    data = get_netblocks()
    json_data = json.dumps(data, indent=4)
    file = open(create_filename(), "w")
    file.write(json_data)
    file.close()


def output_to_csv():
    d1 = get_netblocks()
    d2 = d1['result']['inetnums']
    
    #convert response to json string and parse the json object
    json_arr = json.dumps(d2)
    json_data = json.loads(json_arr)

    #setting headers and rows for the csv file
    cols = ['inetnum', 'netname', 'description', 'org']
    data = json_data

    #open csv file and write specified keys as headers and their values as rows, this still needs tidying
    with open (create_filename(), 'w', newline='') as f:
        wr = csv.DictWriter(f, fieldnames = cols, extrasaction='ignore') 
        wr.writeheader() 
        wr.writerows(data)


def clean_output():
    #cleans output and prints all returned information which is relevant to the console
    netblocks = get_netblocks()
    try:
        raw = netblocks['result']
    except KeyError:
        print("[!] No data returned. Check API key is valid.")
        sys.exit(-1)
    if raw['count'] == 0:
        print("No results for " + args.org)
        sys.exit(-1)
    else:
        sorted_data = netblocks['result']['inetnums']
        block = "\n".join([sub['inetnum'] for sub in sorted_data])
        netname = "\n".join([ sub['netname'] for sub in sorted_data ])
        #if len([sub['description'] for sub in sorted_data]) != 0:
        try:
            des_list = [sub['description'] for sub in sorted_data ]
            my_dt = pd.DataFrame(des_list)
            new_list = [i[0] for i in my_dt.values.tolist()]
            des_str = str(new_list)[1:-1]
            des_stripped = des_str.replace(', ', '\n')
            description = des_stripped.replace("'",'')
        except:
            description = ''
        #descr_2 = re.sub(r'[', '', desc_sorted)
        try:
            org_list = [sub['org']['name'] for sub in sorted_data ]
            org_str = str(org_list)[1:-1]
            org_stripped = org_str.replace(', ', '\n')
            org = org_stripped.replace("'",'')             
        except:
            org = ''       

        output = [[block, netname, description, org]]
        print (tabulate(output, headers=["Netblock", "Block Name", "Description", "Organisation Name"]))


def main():
    clean_output()
    if args.out_csv:
        output_to_csv()
    if args.out_json:
        output_to_json()   


if __name__ == '__main__':
    main()
