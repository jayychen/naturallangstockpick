#!/bin/bash
function kill_proc_with_kw() {
  #can have up to two keywords
  ps -ef | grep "$1" | grep "$2" | grep -v grep | awk '{print $2}' | xargs -I{} kill -9 {}
}

#usage proc_with_kw_exists key_word && echo "exists" || echo "not exist" 
function proc_with_kw_exists() {
  #can have up to two keywords
  pid=`ps -ef | grep "$1" | grep "$2" | grep -v grep | awk '{print $2}'`
  [ ! -z "$pid" ] 
}

function append_to_path() {
  local dir=$1
  case ":$PATH:" in
    *":$dir:"*) ;; # already there
    *) export PATH=$dir:$PATH ;;
  esac
}

function append_to_python_path() {
  local dir=$1
  case ":$PYTHONPATH:" in
    *":$dir:"*) ;; # already there
    *) export PYTHONPATH=$dir:$PYTHONPATH ;;
  esac
}

function append_to_lib_path() {
  local dir=$1
  case ":$LD_LIBRARY_PATH:" in
    *":$dir:"*) ;; # already there
    *) export LD_LIBRARY_PATH=$dir:$LD_LIBRARY_PATH ;;
  esac
}
