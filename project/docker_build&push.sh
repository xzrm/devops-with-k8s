#!/bin/sh
IMAGE="flask-app"
cd ./backend-app
docker build  -t "xzarem/${IMAGE}:${IMAGE}" .
docker push "xzarem/${IMAGE}:${IMAGE}"
SHA256=$(docker inspect --format='{{index .RepoDigests 0}}' "xzarem/${IMAGE}:${IMAGE}" | sed 's/^.*sha256:\(.*\)$/\1/')
echo "$SHA256"
cd ..
cd ./manifest
sed "s/imageTag/${SHA256}/g" flask-app_template.yaml > flask-app.yaml




none_images=$(docker images --filter "dangling=true" -q --no-trunc)

#checking if none_images variable is of type string
# length zero or empty
if [ -z "$none_images" ]
then
    echo "skipping"
else
    docker rmi ${none_images}
fi

