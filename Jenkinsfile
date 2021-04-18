pipeline {
    agent any
    environment {
        DOCKER_TAG = getDockerTag()
    }
    stages {
        stage("Building Docker Image"){
            steps{
                echo "Hello world"
                echo "${DOCKER_TAG}"
            }
        }
    }
}

def getDockerTag(){
    def tag = sh script: 'get rev-parse HEAD', returnStdout: true
    return tag
}