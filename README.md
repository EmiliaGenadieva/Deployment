# Deployment
This repo contains code files needed for the task : <b>Deploy a web-service to Render.</b>
## Task description:
- Deploy API endpoint to the web. Show the results after querying the API in json format.
- Use web technology Flask to process the request from the input fields and display the results.
- Use ML model to predict a price from the given data.

#### Task was resolved by taking the following steps:  
- Create a simple website which shows the result for a predicted price.
Needed are at least 2 web pages found as : [home.html](/templates/home.html) and [index.html](/templates/index.html)
 1. index.html takes the input values from the form.
 2. These values are processed in the python file from the pretrained ML model and a prediction is printed back in home.html (in this html code the value is in the header so it can be noticed quicker)
- The output of json can be displayed after choosing web-service url /dict 
## List of requirements to deploy to Render:
- requirements.txt : install the necessary Python packages
- render.yaml : configuration file
- app.py : Python file as entry point 
- wsgi.py : defines app.run() that the start point is in app.py

## Deployment cycle and consecutive steps taken:
- code is first tested locally by running Flask server
- code was tested with gunicorn
- created repository in Github and connected the repository to Render.com
> The Render Webplatform is easy to use and gives documentation how to deploy.
> There is example how to create the render.yaml file. 
> After creating the web-service one can preview how the image is processed and see errors as well as missing requirements.
