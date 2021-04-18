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
                sh 'docker build . -t xzarem/string-gen:string-gen -f "${WORKSPACE}/main app/main/Dockerfile" ' 
            }
        }
    }
}

def getDockerTag(){
    def tag = sh script: 'git rev-parse HEAD', returnStdout: true
    return tag
}
