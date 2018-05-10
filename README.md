# UIUC Event Recommender

This is a course project for CS410, Spring 2018.

# Goal

Goal of this project is to provide UIUC students a platform where they can receive their personalized event list. 
Given there are so many events in UIUC, it is very hard for someone to track all the events from different departments.
As a result, this event recommender system will push events based on user profile, and update the user profile based on
feedback.

# Demo
http://uiuc-event-recommender.eastus.cloudapp.azure.com/

# Deployment

This is a flask app using python3. Make sure you have these programs installed before you run the app. 
Note the below only works on linux and mac. First make sure you are in the correct folder. 
You should see the flaskr and instance folders. When you are in the correct folder, run the following commands in your terminal.
After you run these, go to http://127.0.0.1:5000/ on your browser to see the working app.


    export FLASK_APP=flaskr
    export FLASK_ENV=development
    python3 -m flask init-db
    python3 -m flask run


After verifying the server is running correctly. Ctrl+C to shutdown server.

If you want to deploy it so that it can be accessed remotely, we have provided a simple script 

    run.sh

Run the script to start server at 0.0.0.0 with port 80. You will need sudo for this command.

# Documentaion

Full documentation can be found in the [Wiki](https://github.com/yuting-zhang/event-recommender/wiki) section of this repository.

# Video Presentation

Video presentation for this project can be found here [link to be added]. Note you need UIUC account to open this link.

# Contributors

Yuting Zhang - Data scraping, recommender framework.

Lan Dao - Data preprocessing, feedback updating.

Shunping Xie - Flask server, BM25

# MIT License

Copyright (c) 2018 Yuting Zhang, Lan Dao, Shunping Xie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
