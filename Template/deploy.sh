#!/bin/bash
#
# This file is part of CSE 489/589 Grader.
#
# CSE 489/589 Grader is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# CSE 489/589 Grader is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with CSE 489/589 Grader. If not, see <http://www.gnu.org/licenses/>.
#

if [ "$#" -ne 3 ]; then
    echo "Usage: deploy HOSTNAME USER PATH"
    exit
fi

hostname=$1
user=$2
path=$3

# Package
cd C && tar -c ubitname/ -f assignment1_template_c.tar --exclude-vcs
cd ..
cd C++ && tar -c ubitname/ -f assignment1_template_cpp.tar --exclude-vcs
cd ..

# Build the grader
mkdir -p grader
./build_grader_exec.sh

# Replace hostname inside scripts
cp assignment1_init_script assignment1_init_script.sh
sed -i "s/host/$hostname/g" assignment1_init_script.sh
cp assignment1_update_grader assignment1_update_grader.sh
sed -i "s/host/$hostname/g" assignment1_update_grader.sh

# Upload
scp C/assignment1_template_c.tar C++/assignment1_template_cpp.tar assignment1_init_script.sh assignment1_update_grader.sh $user@$hostname:$path
scp -r grader $user@$hostname:$path/

rm C/assignment1_template_c.tar
rm C++/assignment1_template_cpp.tar
