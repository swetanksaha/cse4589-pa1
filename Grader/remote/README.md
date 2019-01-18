# CSE 4/589: PA1 AutoGrader [Server]

## Requirements
* GNU **make** and **GCC** toolchain for both C and C++
* [**expect**](http://expect.sourceforge.net/)
* **Python** 2.7 or higher (Python 3.x is not supported)

## Setup
_The setup instructions below need to be repeated for each of the five grading hosts._

### Directories
The grader requires the following two directories setup on each grading host:

* **_dir-grader_** to host the server-side grader source
* **_dir-submission_** where submissions will be uploaded to, un-tarred, built and tested

#### Notes
* Both these directories should be created with appropriate permissions and should not be world read/write-able in any case.
* Both _dir-grader_ and _dir-submission_ should be created at the same absolute path on each host.
* Once the directories are created, make a note of paths of both the directories. They will be required as configuration on the client side.

***
##### <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>
These paths are already setup for the above listed UB CSE hosts:

* **_dir-grader_** ```/projects/CSE489-GRADER```
* **_dir-submission_** ```/local/CSE489-GRADER```

#### Notes
* _dir-grader_ resides on a disk space that is in fact **shared**/replicated on all five hosts. Any files copied to that directory on one of the machines is immediately available on the others
* If you are an instructor/course staff trying to set this up, you might need to contact CSE-IT to be added to the group that has access to these directories
***

The server side of the grader is essentially a basic HTTP server that accepts commands from the client side of the grader. AutoGrader's client side, however, first uploads the submission being tested on each of the grading hosts. The grading hosts upon receiving the uploaded submission locally unpack and build the submission (using the included Makefile) before starting the grading process. The HTTP server, during startup expects path to two sub-folders located inside the _dir-submission_ directory created earlier:

* **_upload_** where submissions will be uploaded
* **_grading_** where submissions will be unpacked and built

To create the two empty dirs, execute the following with _dir-submission_ as the root directory on each of the five hosts:
```bash
$ rm -rf upload && mkdir upload
$ rm -rf grading && mkdir grading
```
***
##### <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>
```bash
$ rm -rf /local/CSE489-GRADER/upload && mkdir /local/CSE489-GRADER/upload && chmod g+w,o-rwx /local/CSE489-GRADER/upload
$ rm -rf /local/CSE489-GRADER/grading && mkdir /local/CSE489-GRADER/grading && chmod g+w,o-rwx /local/CSE489-GRADER/grading
```

#### Notes
* _dir-submission_ resides on a disk that is local to each host, so the directories need to be created individually on each of the five hosts.
* You can decide to skip this step for now, if you plan to use the quick server startup script mentioned at very [end](https://github.com/cse4589/cse4589-pa1/tree/master/Grader/remote#-4) of this guide in the [start](https://github.com/cse4589/cse4589-pa1/tree/master/Grader/remote#start) section, which takes care of folder creation.
***

### Install
Execute the following with _dir-grader_ as the root directory on each of the five hosts:
```bash
$ mkdir pa1_http_server
$ cd pa1_http_server
$ git clone --no-checkout https://github.com/cse4589/cse4589-pa1.git
$ cd cse4589-pa1
$ git config core.sparseCheckout true
$ echo 'Grader/remote' >> .git/info/sparse-checkout
$ echo 'HTTPLauncher' >> .git/info/sparse-checkout
$ git checkout master
```

***
##### <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>
Since _dir-grader_ is shared among the five hosts, this steps need to be followed only **once** on any _one_ of the grading hosts.
***

### Start
The server can be started at port number [port] as follows:
```bash
$ cd HTTPLauncher
$ python grader_launcher.py -p [port] -u /path/to/dir-submission/upload -g /path/to/dir-submission/grading
```

#### Notes
* The server **MUST** be started by the same user that created all the directories OR permissions should be setup in such a way that the server process has read and write access to all the directories created above.
* During grading, new processes will be spawned which will be owned by the user starting the server process. The user starting this process might end up with a large number of active processes if multiple submissions are tested at the same time.
* This server needs to run indefinitely, you would typically run it in daemon/detached mode using something like the [screen](https://www.gnu.org/software/screen/) utility. You can look at the UB specific instructions below to get an idea and then adapt it for your installation.

***
##### <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>

To make the server start/restart easier within UB CSE department, you can use our quick server startup script. To start the script on port number [port]:

```bash
$ wget https://git.io/fh0vk -O start_pa1_http_server.sh
$ chmod +x start_pa1_http_server.sh
$ screen -d -m /absolute/path/to/start_pa1_http_server.sh [port]
```

***

#### Notes
* The startup procedure needs to be repeated on all the grading hosts.
* Make note of the port number used to start the Autograder's server. It will be used to configure the AutoGrader's client.
