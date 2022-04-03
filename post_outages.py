import requests
import json
import pandas as pd
import sys

_, site_id, api_key = sys.argv
headers = {'x-api-key': api_key}

#retrieve all outages
outages_url = f"https://api.krakenflex.systems/interview-tests-mock-api/v1/outages"
outages_response = requests.get(url=outages_url, headers=headers)
outages_res = json.loads(outages_response.text)
outages_df = pd.DataFrame(outages_res)
#filters out any outages that began before `2022-01-01T00:00:00.000Z` 
outages_filter_df = outages_df[outages_df['begin'] >= '2022-01-01T00:00:00.000Z']

#retrieve site-info
site_id='norwich-pear-tree'
site_url = f"https://api.krakenflex.systems/interview-tests-mock-api/v1/site-info/{site_id}"
site_response = requests.get(url=site_url, headers=headers)
site_res = json.loads(site_response.text)
site_df = pd.DataFrame(site_res["devices"])

#mergeing only id from site and adding name column
merge_df = outages_filter_df.merge(site_df, on='id', how='inner')
#dataframe to json
merge_js = merge_df[['id', 'name', 'begin', 'end']].to_json(orient = 'records')

#send post site outages
post_outages_url = f"https://api.krakenflex.systems/interview-tests-mock-api/v1/site-outages/{site_id}"
post_outages_response = requests.post(url=site_url, json=merge_js, headers=headers)