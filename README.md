# qradar-aqlcodegen-app
This QRadar application generated the AQL query from the normal language statement.


QRadar SDK documentation ``` https://www.ibm.com/support/pages/qradar-whats-new-app-framework-sdk-v200 ```

how to install QRadar SDK ``` https://www.ibm.com/support/pages/qradar-whats-new-app-framework-sdk-v200#i ```


### Suggested changes needs to be done before deployment: ###

* Update the token and BASE_URL for the user's watsonx instance in views.py 

* Very few training samples are added for the Model. Can update the samples based on the use cases.



To install the app on QRadar using the SDK, follow these simple steps:

Step 1: Identify Default Server and User Values (Optional)

``` qapp server -q <QRadar_server> -u <QRadar_user> ```

Step 2: Package the App

``` qapp package -p com.mycompany.myapp.zip ```

Step 3: Deploy the App to QRadar

``` qapp deploy -q <QRadar_server> -u <QRadar_user> -p com.mycompany.myapp.zip ```

Note: “Replace <QRadar_server> with the IP or hostname of your QRadar console and <QRadar_user> with the username of a user with the necessary permissions to deploy apps. The app will be uploaded to QRadar and installed for use."

---> Route To run on QRadar ---> @viewsbp.route('/index', methods=['GET', 'POST']) # for QRadar

---> Route To run on Docker locally  ---> @viewsbp.route('/', methods=['GET', 'POST']) # for Local system
