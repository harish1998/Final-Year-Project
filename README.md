# Final-Year-Project
A Software Defined Networking **(SDN)** based Video Classification System
## Motivation
This Project was done as part of my Undergraduate CourseWork
## Description
In University, Video sites like YouTube are completely blocked regardless of their Content. This hinders the access to Educational Content across YouTube. In order to overcome this,A SDN based Video Classification System that categorizes YouTube Videos to either Entertainment or Education category thereby determining their access was implemented.
## Installation
To Set up this project, You need following
```
Ubuntu 16.04 or greater
Python 3.6 or greater
ScikitLearn
Pandas
NLTK
Ryu
Mininet
google-api-python-client
Postman
```
## Usage
Run in the following Order
```
python Train.py
```
This will generate the serialized model and vector files that further will be used by Test.py
Then, Start Mininet using the following command
```
sudo mn --controller=remote,ip=127.0.0.1,port=4545
h1 python -m SimpleHTTPServer 80 &
xterm h1, h2

```

Now, start Ryu Remote Controller
```
ryu-manager --verbose ryu/app/Controller.py
```
In the Xterm window of h1, give YouTube video ID as 
```wget 10.0.0.2/videoID```

## Reference

[Ryu Documentation] (https://ryu.readthedocs.io/en/latest/) <br>
[Mininet Docs] (http://mininet.org/walkthrough/) <br>
[DataSet Link] (https://www.curiousgnu.com/youtube-comments-text-analysis) <br>
[Useful Tut] (https://inside-openflow.com/2016/06/23/interactive-ryu-with-postman/)
