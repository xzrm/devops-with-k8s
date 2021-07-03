#!/bin/sh
none_images=$(docker images --filter "dangling=true" -q --no-trunc)

if [ -z "$none_images" ]
then
    echo "skipping"
else
    docker rmi ${none_images}
fi