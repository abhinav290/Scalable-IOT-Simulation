# Scalable-IOT-Simulation

Simulation for IOT Body area network.

## Tech Stack
Technologies used in this simulation,

* Python - For writing the code for all nodes and their features.
* AMAZON SQS - For data communication.
* AngularJS - For creating the dashboard.

And project is present in a [public repository][repo] on GitHub.
<<<<<<< HEAD
=======

## Code Structure
### Directories
The directories listed inside iot package are discussed in brief here

| Directory | Coontents |
| ------ | ------ |
|  body1  | Code for sensors and sink inside a body. |
|  body1/sensors  | Sensors and their condfiguration (config) according to their ids. |
|  body1/sink  | Sink and its configuration. |
|  critical_edge_node  | Code for edge device responsible for handling critical data. |
|  edge_node  | Code for edge device for handling normal data and scripts for uploading and downloading data to Amazon S3 Bucket. |
|  body1/sink  | Sink and its condfiguration. |


## Setup and Execution
>>>>>>> 9e233426d3dc982fb5b84763f82a45e38266a83b
### Installation

This project requires Python3 to run.

Install Python3 and required pip packages.

```sh
$ pip install boto3
```

For dashboard NodeJS, AngularJS and its dependencies are required.

```sh
$ npm install 
$ NODE_ENV=production node app
```

<<<<<<< HEAD
## Code Structure
### Directories
The directories listed inside iot package are discussed in brief here

| Directory | Coontents |
| ------ | ------ |
|  body1  | Code for sensors and sink inside a body. |
|  body1/sensors  | Sensors and their condfiguration (config) according to their ids. |
|  body1/sink  | Sink and its configuration. |
|  critical_edge_node  | Code for edge device responsible for handling critical data. |
|  edge_node  | Code for edge device for handling normal data and scripts for uploading and downloading data to Amazon S3 Bucket. |
|  utils  | Communication utilities for AMAZON S3 and SQS. |
Sample config of a sensor:-

```javascript
{   "type": "Blood Pressure", 
    "battery": 65.37704081792825, 
    "duty_cycle": 1, 
    "data_rate": 2, 
    "status": true, 
    "transmission_cycle": 3, 
    "active_power": 0.0005, 
    "transmission_power": 0.0007, 
    "distance_to_sink": 7
}
```
Parameter Meaning
> Battery is the remaining battery in percentage.
> Duty cycle is represented in percentage. For example, 1 means 1 %.
> Data Rate is bytes of data that can be transmiited per second.
> Status represents if the sensor is on or off.
> Transmission cycle is used to transmit data to forwarder node every nth cycle.
> Active Power is power loss per second.
> Transmission_power is power loss per second when sensor is sending data.

## Setup and Execution
* Create an account on AWS and generate private and secret key and store it in your system. Further information can be found [here][aws_access_help]. 
* Create AWS S3 Bucket for storing data. Please update this bucket name in download_s3_file.py and upload_to_s3.py in iot/edge_node directory.
* Create 4 AWS SQS FIFO Queues and while configuring the queues select Content Duplication.
    * Queue1 - Sensor To Forwarder
        * Update in iot/body1/sensors/sensor.py 
    * Queue2 - Sensor To Sink
        * Update in iot/body1/sensors/sensor.py 
        * Update in iot/body1/sensors/sink.py 
    * Queue3 - Sink to Edge
        * Update in iot/body1/sensors/sink.py 
        * Update in iot/body1/edge_node/base.py 
    * Queue4 - Sink to Edge (Critical Data)
        * Update in iot/body1/sensors/sink.py 
        * Update in iot/critical_edge/base.py 


### Execution
1. Run `iot/edge_node/base.py` to start edge node.
2. Run `iot/edge/critical_edge/base.py` to start the critical edge node.
3. Run `iot/body1/sink/sink.py` to start the sink node. 
4. Set the `status` in the `config` file of the sensor you want to start and run its corresponding python script.
5. Once simulation is done run `iot/edge_node/upload_to_s3.py` to upload the data to S3 bucket after updating the bucket name in the script.
6. To display the data on the dashboard run `iot/edge/download_s3_file.py` after updating the bucket name and file path for your system.

Simulation ends here.
=======
### Development

>>>>>>> 9e233426d3dc982fb5b84763f82a45e38266a83b


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen.)


   [repo]: <https://github.com/abhinav290/Scalable-IOT-Simulation>
<<<<<<< HEAD
   [aws_access_help]: <https://www.cloudberrylab.com/resources/blog/how-to-find-your-aws-access-key-id-and-secret-access-key>
=======
>>>>>>> 9e233426d3dc982fb5b84763f82a45e38266a83b
