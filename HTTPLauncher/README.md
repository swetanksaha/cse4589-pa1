# CSE 4/589: PA1 Grader [HTTPLauncher]

## Setup
```bash
$ git clone -b student --no-checkout https://ubwins.cse.buffalo.edu/git/swetankk/cse4589_pa1.git
$ cd cse4589_pa1
$ git config core.sparseCheckout true
$ echo 'HTTPLauncher' >> .git/info/sparse-checkout
$ git checkout student
```

## Run

```bash
$ cd HTTPLauncher
$ python grader_launcher.py -p PORT -u UPLOAD_DIR -g GRADING_DIR
```
**UPLOAD_DIR** Path to directory to store upoaded submission (.tar) files.

**GRADING_DIR** Path to directory where submissions are unpackaged and built before grading.

*Note that the HTTPLauncher would typically be run a as background service/daemon.*
