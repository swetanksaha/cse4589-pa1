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
# Dependencies: gnome, sshpass, ssh, gui

grading_server_list=$1
remote_grader_path=$2
port=$3

user=$4
id=$5

cmd="gnome-terminal --maximize "
IFS=","
for server in $grading_server_list
do
    cmd+="--tab --command 'ssh -i ${id} ${user}@${server} -t \"cd ${remote_grader_path};killall grader_remote.py;./grader_remote.py -p ${port};/bin/tcsh\"' "
done

echo $cmd
eval $cmd