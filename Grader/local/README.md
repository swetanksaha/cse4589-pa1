# CSE 4/589: PA1 AutoGrader [Client]

Note that you need to follow the instructions below **ONLY** if you want to run the grader (client side) from source for debugging purposes or you are trying to re-package after making changes or package it into a binary for a non-Linux platform.

Typically, you do **NOT** need to specifically provide even the binary version (or a link to download it) to the students. The main assignment description/handout provided to students already contains the download link and instructions for its usage.

However, note that grader requires some configuration items (port number of the server, etc.) that need to be provided to the students (details below). Such configuration can be distributed to the students through typical course communication channels (piazza, course website, etc.).

## Setup
You need to follow the steps below only if you want to run the grader from the source. If you are using the binary version, skip to the [Configure](https://github.com/cse4589/cse4589-pa1/blob/master/Grader/local/README.md#configure) section.

```bash
$ git clone --no-checkout https://github.com/cse4589/cse4589-pa1.git
$ cd cse4589-pa1
$ git config core.sparseCheckout true
$ echo 'Grader/local' >> .git/info/sparse-checkout
$ git checkout master
```

## Configure
Before the AutoGrader's client can talk to the server, it needs to be configured. Client's configuration is contained in ```Grader/local/grader.cfg```. Available configuration options are explained below.

### Configuration Options

* [GradingServerList]
  * **server-1 ... server-5** _FQDNs of the five grading host machines._

* [HTTPLauncher]
  * **port** _Port number the AutoGrader server was started on._ This is the port number you used at the last [step](https://github.com/cse4589/cse4589-pa1/tree/master/Grader/remote#start) in the server setup process.

* [GradingServer]
  * **path-python** _Absolute path on the servers to a python installation_.
  * **dir-grader** _Absolute path on the servers to the grader directory created during the server setup [steps](https://github.com/cse4589/cse4589-pa1/tree/master/Grader/remote#directories)._
  * **dir-submission** _Absolute path on the servers to the submission directory created during the server setup [steps](https://github.com/cse4589/cse4589-pa1/tree/master/Grader/remote#directories)._

* [Grader]
  * **binary** _Filename of the binary created by the submission Makefile (default=assignment1)._ This is an internal grader property and does not require any changes to it.

***
##### <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>
The binary client downloaded by students through the link provided in the assignment handout contains a pre-configured grader.cfg. It comes populated with values assuming the server setup process detailed  [here](https://github.com/cse4589/cse4589-pa1/blob/master/Grader/remote/README.md) was followed.

However, the **port** value still needs to updated. This **NEEDS** be provided to the students by the instructor/course staff, after completing server setup through course communication channels (piazza, course website, etc.). This is the _ONLY_ value the students would need to input/edit in the grader.cfg.
***

## Run
This step assumes that the five server instances are already setup and running. If the server component is not setup, please follow the steps listed [here](/Grader/remote).

```bash
$ cd Grader/local
$ ./grader_controller.py -c CONFIG -s SUBMISSION -t TEST [-nu] [-nb]
```

The binary version (created using the steps detailed below) can be run similarly as:

```bash
$ ./grader_controller -c CONFIG -s SUBMISSION -t TEST [-nu] [-nb]
```

## Convert to Binary
We make use of the [pyinstaller](http://www.pyinstaller.org/) package to convert AutoGrader's client side python scripts into a single executable binary.

You need to first obtain the source of the grader, using instructions listed above under the [Setup](https://github.com/cse4589/cse4589-pa1/tree/master/Grader/local#setup) section. To convert to binary, execute the following with the ```Grader/local/``` as the root directory.

```bash
$ pyinstaller --onefile grader_controller.py
```

If everything goes well, the executable named _grader_controller_ will be created ```Grader/local/dist``` directory. You can upload this binary and the grader.cfg to somewhere it can be publicly downloaded from.

***
##### <img src="http://cse4589.github.io/assets/site/images/UB_BLU_RGB.png" width=30></img>
In all likelihood, there is no need for this conversion as pre-compiled binaries are already available for UB students to be downloaded. The download and setup is taken care by the template scripts which are documented in the assignment handout/description. Remember that students still **NEED** to be notified of the server's port number before they can use the AutoGrader.
***
