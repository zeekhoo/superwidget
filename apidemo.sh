#!/bin/sh
# This script can be used to simplify starting and stopping the API Demo Docker container.
# ./apidemo.sh start
# ./apidemo.sh stop
# ./apidemo.sh status
# ./apidemo.sh cleanup

SERVER_CONTAINER="zzkhoo/okta-api-demo:latest"
PWD=$(pwd)
STATIC_PATH="$PWD/static"
DOCKER_STATIC_PATH="/okta_api_demo/static"

CONTAINER_ID=$(docker ps -a | grep Created | grep $SERVER_CONTAINER | awk '{print $1}')
    	if [[ -n $CONTAINER_ID ]] ; then
    		Echo "----- Docker container found in CREATED status, please run ./`basename $0` cleanup -----"
    	fi

function getStatus(){
    CONTAINER_ID=$(docker ps -a | grep -v Exit | grep $SERVER_CONTAINER | awk '{print $1}')
    if [[ -z $CONTAINER_ID ]] ; then
        echo 'Not running.'
    else
        echo "API Demo is currently running with container ID: $CONTAINER_ID"
    fi
}

case "$1" in
    start)
    	CONTAINER_ID=$(docker ps -a | grep -v Exit | grep $SERVER_CONTAINER | awk '{print $1}')
    	if [[ -z $CONTAINER_ID ]] ; then
    		echo "Starting Docker API Demo"
        	docker run -p 8000:8000 --env-file=env.list -v $STATIC_PATH:$DOCKER_STATIC_PATH -t zzkhoo/okta-api-demo:latest
        	getStatus
    	else
        	getStatus
    	fi
        ;;

    status)
        getStatus
        ;;

    cleanup)
	echo "Cleaning up all inactive and stopped Docker containers"
	docker ps -aq --no-trunc | xargs docker rm
	;;
    stop)
        CONTAINER_ID=$(docker ps -a | grep -v Exit | grep $SERVER_CONTAINER | awk '{print $1}')
        if [[ -n $CONTAINER_ID ]] ; then
            SRV=$(docker stop $CONTAINER_ID)
            if [ $? -eq 0 ] ; then
                echo 'Stopped.'
            fi
        else
            echo 'Not Running.'
            exit 1
        fi
        ;;

    *)
        echo "Usage: `basename $0`  {start|stop|status|cleanup}"
        exit 1
        ;;
esac

exit 0
