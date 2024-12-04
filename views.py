# Licensed Materials - Property of IBM
# 5725I71-CC011829
# (C) Copyright IBM Corp. 2015, 2020. All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

from flask import Flask, Blueprint, render_template, current_app, send_from_directory, redirect, url_for, request
from qpylib import qpylib
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import requests

# pylint: disable=invalid-name
viewsbp = Blueprint('viewsbp', __name__, url_prefix='/')



@viewsbp.route('/index', methods=['POST', 'GET'])
def execute():
    if request.method == 'POST':
        aql_stm = request.form['nm']
        text = aql_stm.strip()
        token = 'Add token here'
        authenticator = IAMAuthenticator(token)
        access_token = authenticator.token_manager.get_token()

        if len(text) > 1:
            HEADERS = {
                'accept': 'application/json',
                'content-type': 'application/json',
                'Authorization': 'Bearer {}'.format(access_token)
            }
            
            BASE_URL = 'Add Base Url here'
            REQ_URL = BASE_URL + '/ml/v1/text/generation?version=2023-05-29'
            payload_f_json = {
        
                "input": """Convert the natural language statement into Ariel Query Language

                    Input: Select all events
                    Output: SELECT * from events

                    Input: Select all events group by source ip
                    Output: SELECT * from events Group By sourceIp

                    Input: Give count of all events
                    Output: SELECT COUNT(*) from events

                    Input: Search username, unique count of source ip from events group by source ip
                    Output: SELECT username, UNIQUECOUNT(sourceip) FROM events GROUP BY sourceip
                    
                    Input: Search username, source ip and domain name from domain id from events
                    Output: SELECT sourceip, username, DOMAINNAME(domainid) FROM events

                    Input: Search source ip, destination ip and geo distance from events in last 10 minutes
                    Output: SELECT sourceip, destinationip, GEO::DISTANCE(sourceip, destinationip) FROM events LAST 10 minutes

                    Input: Search all the events from 1 hour ago till now group by source ip
                    Output: SELECT * from events Group By sourceip START PARSEDATETIME('1 hour ago') STOP PARSEDATETIME('now')
                    
                    Input: Select sourceip and protocol name from events
                    Output: SELECT sourceip, PROTOCOLNAME(protocolid) FROM events""",
                    

                "model_id": "ibm/granite-20b-code-instruct",
                "project_id": "Add ProjectId here",
                "parameters": {
                    "decoding_method": "greedy",
                    "stop_sequences": [
                    "\n"
                    ],
                    "include_stop_sequence": False,
                    "min_new_tokens": 1,
                    "max_new_tokens": 4096
                },
                "moderations": {
                    "hap": {
                    "input": {
                        "enabled": True,
                        "threshold": 0.75
                    },
                    "output": {
                        "enabled": True,
                        "threshold": 0.75
                    }
                    }
                },
                "prompt_id": "prompt_builder",
            }
            # payload_f_json['inputs'] = [text]
            payload_f_json['input'] = payload_f_json['input']+text+"\n\nOutput:\n"
            response_llm = requests.post(REQ_URL, headers=HEADERS, data=json.dumps(payload_f_json))
            response_llm_json = response_llm.json()
            answer = response_llm_json['results'][0]['generated_text']
            return render_template('index.html', name=text, ans=answer)
        else:
            user = request.args.get('nm')
            return render_template('index.html')
    else:
        user = request.args.get('nm')
        return render_template('index.html')


# The presence of this endpoint avoids a Flask error being logged when a browser
# makes a favicon.ico request. It demonstrates use of send_from_directory
# and current_app.
@viewsbp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'favicon-16x16.png')
