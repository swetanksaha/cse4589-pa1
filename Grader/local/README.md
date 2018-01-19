# CSE 4/589: PA1 AutoGrader [Client]

Note that you need to follow the instructions below **ONLY** if you want to run the grader (client side) from source for debugging purposes or you are trying to re-package after making changes or package it into a binary for a non-Linux platform.

Typically, you do **NOT** need to specifically provide even the binary (or a link to download it) version to the students. The main assignment description/handout, provided to students, already contains the download link and instructions for its usage.

However, note that grader requires some configuration items (port number of the server etc.) that need to be provided to the students (details below). Such configuration can be distributed to the students through typical course communication (piazza, course website etc.).

## Setup
You need to follow the steps below only if you want to run the grader from the source.

```bash
$ git clone --no-checkout https://github.com/cse4589/cse4589-pa1.git
$ cd cse4589_pa1
$ git config core.sparseCheckout true
$ echo 'Grader/local/' >> .git/info/sparse-checkout
$ git checkout master
```

## Configure
Before the AutoGrader's client can talk to the server, it needs to be configured.

## Run
This step assumes that the five server instances are already setup and running. If the server component is not setup, please follow the steps listed [here](/Grader/remote).

```bash
$ cd Grader/local
$ ./grader_controller.py -c CONFIG -s SUBMISSION -t TEST [-nu] [-nb]
```

## Convert to Binary
