pipeline {
    agent any
    stages {
        stage("Building Docker Image"){
            steps{
                dir("${WORKSPACE}/main app/main") {
                    sh "pwd"
                    sh "docker build . -t xzarem/string-gen:${env.GIT_COMMIT}" 
                 }
            }
        }
    }
}
