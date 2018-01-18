# CSE 4/589: PA1 AutoGrader [Client]

Note that you need to follow the instructions below only if you want to run the grader (client side) from source for debugging purposes or you are trying to package it into a binary for a non-Linux platform.

Binary for the Linux-based OS is directly available for download [here](). Also, note that you don't to specifically provide this binary (or a link to download it) to the students. The main assignment description/handout, provided to students, already contains the download link and instructions for its usage.

## Setup
```bash
$ git clone --no-checkout https://ubwins.cse.buffalo.edu/git/swetankk/cse4589_pa1.git
$ cd cse4589_pa1
$ git config core.sparseCheckout true
$ echo 'Grader/local/' >> .git/info/sparse-checkout
$ git checkout master
```

## Run
This step assumes that the five server instances are already setup and running.

```bash
$ cd Grader/local
$ ./grader_controller.py -c CONFIG -s STUDENT -t TEST
```

## Convert to Binary
