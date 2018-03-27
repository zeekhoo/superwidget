#!/bin/sh
# This script can be used to simplify starting and stopping the API Demo Docker container.
# ./apidemo.sh start
# ./apidemo.sh stop
# ./apidemo.sh status

SERVER_CONTAINER="zzkhoo/okta-api-demo:latest"

function getStatus(){
    CONTAINER_ID=$(docker ps -a | grep -v Exit | grep $SERVER_CONTAINER | awk '{print $1}')
    if [[ -z $CONTAINER_ID ]] ; then
        echo 'Not running.'
        return 1
    else
        echo "Running in container: $CONTAINER_ID"
        return 0
    fi
}

case "$1" in
    start)

    	CONTAINER_ID=$(docker ps -a | grep -v Exit | grep $SERVER_CONTAINER | awk '{print $1}')
    	if [[ -z $CONTAINER_ID ]] ; then
		echo "Starting Docker API Demo"
        	docker run -p 8000:8000 --env-file=env.list -t zzkhoo/okta-api-demo:latest
        	return 1
    	else
        	echo "Running in container: $CONTAINER_ID"
        	return 0
    	fi

        getStatus
        ;;

    status)
        getStatus
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
        echo "Usage: `basename $0`  {start|stop|status}"
        exit 1
        ;;
esac

exit 0
