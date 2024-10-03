# Licensed Materials - Property of IBM
# 5725I71-CC011829
# (C) Copyright IBM Corp. 2015, 2020. All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.

from flask import Flask, Blueprint, render_template, current_app, send_from_directory, redirect, url_for, request
from qpylib import qpylib
import json
import requests

# pylint: disable=invalid-name
viewsbp = Blueprint('viewsbp', __name__, url_prefix='/')

@viewsbp.route('/index', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        aql_stm = request.form['nm']
        text = aql_stm.strip()
        token = 'Add the token here'
        if len(text) > 1:
            HEADERS = {
                'accept': 'application/json',
                'content-type': 'application/json',
                'Authorization': 'Bearer' + token
            }
            BASE_URL = 'https://bam-api.res.ibm.com'
            REQ_URL = BASE_URL + '/v2/text/generation?version=2024-04-15'
            payload_f_json = {
                "model_id": "ibm/granite-20b-code-instruct-v1",
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
                "data": {
                    "input": "",
                    "instruction": "Extract PII entities from the text given",
                    "input_prefix": "Input:",
                    "output_prefix": "Output:",
                    "examples": [
                        {
                            "input": "Select all events",
                            "output": "SELECT * from events"
                        },
                        {
                            "input": "Select all events group by source ip",
                            "output": "SELECT * from events Group By sourceIp "
                        },
                        {
                            "input": "Give count of all events",
                            "output": "SELECT COUNT(*) from events"
                        },
                        {
                            "input": "Search username, unique count of source ip from events group by source ip",
                            "output": "SELECT username, UNIQUECOUNT(sourceip) FROM events GROUP BY sourceip"
                        },
                        {
                            "input": "Search username, source ip and domain name from domain id from events",
                            "output": "SELECT sourceip, username, DOMAINNAME(domainid) FROM events"
                        },
                        {
                            "input": "Search source ip, destination ip and geo distance from events in last 10 minutes",
                            "output": "SELECT sourceip, destinationip, GEO::DISTANCE(sourceip, destinationip) FROM events LAST 10 minutes"
                        },
                        {
                            "input": " Search source ip, destination ip and geo distance from events from yesterday 10am to today 11am",
                            "output": "SELECT * FROM EVENTS START '2023-10-17 10:00' STOP '2023-10-18 11:00'"
                        },
                        {
                            "input": "Search all the events from 1 hour ago till now group by source ip",
                            "output": "SELECT * from events Group By sourceip START PARSEDATETIME('1 hour ago') STOP PARSEDATETIME('now')"
                        },
                        {
                            "input": "Select sourceip and protocol name from events",
                            "output": "SELECT sourceip, PROTOCOLNAME(protocolid) FROM events"
                        }
                    ],
                    "system_prompt": "You are Granite Chat, an AI language model developed by IBM. You are a cautious assistant that carefully follows instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior. You respond in a comprehensive manner unless instructed otherwise, providing explanations when needed while maintaining a neutral tone. You are capable of coding, writing, and roleplaying. You are cautious and refrain from generating real-time information, highly subjective or opinion-based topics. You are harmless and refrain from generating content involving any form of bias, violence, discrimination or inappropriate content. You always respond to greetings (for example, hi, hello, g'\''day, morning, afternoon, evening, night, what'\''s up, nice to meet you, sup, etc) with \"Hello! I am Granite Chat, created by IBM. How can I help you today?\". Please do not say anything else and do not start a conversation."
                }
            }
            # payload_f_json['inputs'] = [text]
            payload_f_json["data"]['input'] = [text]
            response_llm = requests.post(REQ_URL, headers=HEADERS, data=json.dumps(payload_f_json))
            response_llm_json = response_llm.json()
            answer = response_llm_json['error']
            return render_template('index.html', name=text, ans=answer)
        else:
            user = request.args.get('nm')
            return render_template('index.html')
    else:
        user = request.args.get('nm')
        print('user', user)
        return render_template('index.html')


# The presence of this endpoint avoids a Flask error being logged when a browser
# makes a favicon.ico request. It demonstrates use of send_from_directory
# and current_app.
@viewsbp.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.static_folder, 'favicon-16x16.png')
