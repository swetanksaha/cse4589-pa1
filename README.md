# CSE 4/589: Programming Assignment 1 (PA1) AutoGrader
If you have landed at this repository directly, you first should read up on bit of a background [here](https://cse4589.github.io/).

## Introduction
PA1 AutoGrader itself runs as a distributed server-client application, with multiple server instances deployed (one-time setup) by the course staff and the client side distributed to the students/Teaching Assistants (TAs), which they can use to test the submission and get a score.

The AutoGrader takes as input, on the client side, the student source code which is first uploaded to each of the servers, built and then tested for a given test case.

The [_Grader_](/Grader) directory holds both the client and server components.

The [_Template_](/Template) directory contains the source for the code template distributed to students (see [here](https://docs.google.com/document/d/1Rct0Hv8vmQc6Yub_3SH4ElDkly8rSgNnDKSjrChPjqw)).

## Requirements
* **Five(5)** Linux hosts/machines
* Networking setup such that all the five hosts are _reachable_ from each other

***
<img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>
List of UB CSE hosts:
* stones.cse.buffalo.edu
* euston.cse.buffalo.edu
* embankment.cse.buffalo.edu
* underground.cse.buffalo.edu
* highgate.cse.buffalo.edu
***

## Server
Server source, requirements, and setup instructions are hosted under the [_Grader/remote_](/Grader/remote) directory. The server side is written completely in python and makes use of expect scripts to interact (I/O) with the submission being tested. When run, it exposes an HTTP server which the client uses for all communication.

## Client
Client (distributed to students) source is hosted under the [_Grader/local_](/Grader/local) directory. Note that typically the client side of the grader is distributed as a single executable binary, instead of the raw python source files to avoid imposing any additional setup requirements on student machine environments. Setup instructions include steps to convert the python source to a Linux executable. It should be fairly straightforward to adapt the conversion process for any other OS the course staff wishes to support. In addition, we also include steps to run the grader directly from source to allow for easy debugging.
