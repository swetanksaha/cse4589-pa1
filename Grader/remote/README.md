# CSE 4/589: PA1 AutoGrader [Server]

## Requirements

* **Five(5)** Linux servers/machines
* Networking setup such that all the five servers are _reachable_ from each other
* GNU **make** and **GCC** toolchain for both C and C++
* [**expect**](http://expect.sourceforge.net/)
* **Python** 2.7 or higher (Python 3.x is not supported)

##### Instructions: UB
List of UB CSE servers:
* stones.cse.buffalo.edu
* euston.cse.buffalo.edu
* embankment.cse.buffalo.edu
* underground.cse.buffalo.edu
* highgate.cse.buffalo.edu

> <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>

## Setup
_The setup instructions below need to be repeated for each of the five grading servers._

### Directories
The grader requires the following two directories setup on each server:

* **_dir-grader_** to host the server-side grader source
* **_dir-submission_** where submissions will be uploaded to, un-tarred, built and tested

#### Notes
* Both these directories should be created with appropriate permissions and should not be world read/write-able in any case.
* Both _dir-grader_ and _dir-submission_ should be created at the same absolute on each server.
* Once the directories are created, make a note of paths of both the directories. They will be required as configuration on the client side.

##### Instructions: UB
These paths are already setup for above listed UB servers:

* **_dir-grader_** ```/projects/CSE489-GRADER```
* **_dir-submission_** ```/local/CSE489-GRADER```

Note that the **_dir-grader_** resides on a disk space that is in fact shared/replicated on all five servers. So, any files copied to that directory on one of the servers is immediately available on the others.

> <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>

### Install
