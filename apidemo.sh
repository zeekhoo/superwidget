#!/bin/sh
# This script can be used to simplify starting and stopping the API Demo Docker container.

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
    			echo "----- Starting Docker API Demo as a background process. Docker will continue to run until you stop it. -----"
        		docker run -p 8000:8000 --env-file=env.list -v $STATIC_PATH:$DOCKER_STATIC_PATH -d $SERVER_CONTAINER
        		getStatus
    		else
        		getStatus
    		fi
        ;;
        
	interactive)
    		CONTAINER_ID=$(docker ps -a | grep -v Exit | grep $SERVER_CONTAINER | awk '{print $1}')
    		if [[ -z $CONTAINER_ID ]] ; then
    			echo "----- Starting Docker API Demo in interactive mode, hitting ctrl-c will stop the Docker process. -----"
        		docker run -p 8000:8000 --env-file=env.list -v $STATIC_PATH:$DOCKER_STATIC_PATH -it $SERVER_CONTAINER
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
                		echo "Stopped the API Demo container"
			else
				echo "There was an error when stopping the API Demo container"
            		fi
        	else
        		echo "API Demo container is not running."
        		exit 1
        	fi
        ;;
	
	*)
        	echo "Usage: ./`basename $0`  {start|stop|status}"
        	echo "./`basename $0` start		-- Starts the API container as a background process that will run until stopped"
		echo "./`basename $0` stop 		-- Stops the API Demo container"
		echo "./`basename $0` status		-- Shows if the API Demo is currently running"
		echo "./`basename $0` cleanup		-- Cleans up any old, non-running Docker containers"
		echo "./`basename $0` interactive		-- Runs Docker in interactive mode which terminates when the script is terminated"
        ;;
esac

exit 0
