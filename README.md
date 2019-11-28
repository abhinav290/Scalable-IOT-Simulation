# Scalable-IOT-Simulation

Simulation for IOT Body area network.

## Tech Stack
Technologies used in this simulation,

* Python - For writing the code for all nodes and their features.
* AMAZON SQS - For data communication.
* AngularJS - For creating the dashboard.

And project is present in a [public repository][repo] on GitHub.

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

### Development



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen.)


   [repo]: <https://github.com/abhinav290/Scalable-IOT-Simulation>
