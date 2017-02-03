# CSE 4/589: PA1 Grader [Client]

## Setup
```bash
$ git clone --no-checkout https://ubwins.cse.buffalo.edu/git/swetankk/cse4589_pa1.git
$ cd cse4589_pa1
$ git config core.sparseCheckout true
$ echo 'Grader/local/' >> .git/info/sparse-checkout
$ git checkout master
```

## Run
```bash
$ cd Grader/local
$ ./grader_controller.py -c CONFIG -s STUDENT -t TEST
```
