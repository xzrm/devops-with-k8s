pipeline {
    agent any
    environment {
        DOCKER_TAG = getDockerTag()
    }
    stages {
        stage("Building Docker Image"){
            steps{
                sh 'cd "main app/main" ' 
                sh "pwd"
                echo "${env.GIT_COMMIT}" 
                echo "${WORKSPACE}"
                sh "docker build ./Dockerfile -t xzarem/string-gen:${DOCKER_TAG}"
            }
        }
    }
}

def getDockerTag(){
    def tag = sh script: 'git rev-parse HEAD', returnStdout: true
    return tag
}
