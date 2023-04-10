#!/bin/bash
#environment variable setting file

#root
export PjtDir="${HOME}/project/nlsp"		    #

#shell
source $PjtDir/shell/system.sh
source $PjtDir/shell/run.sh

#system path
append_to_path ${PjtDir}/build/Release/bin #exe
append_to_python_path ${PjtDir}/python

#dir change
function nlsp() { cd $PjtDir ; }

#==========================================================================================
#command pass through
eval "$@"

