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
        stage("Docker hub push"){
            steps{
                withCredentials([string(credentialsId: 'docker-hub', variable: 'DockerHubPwd')]) {
                    sh "docker login -u xzarem -p ${DockerHubPwd}"
                    sh "docker push xzarem/string-gen:${env.GIT_COMMIT}"
                    }               
            }
        }
        stage("Deploy to k8s"){
            steps{
                dir("${WORKSPACE}/main app/manifest") {
                    sh "chmod +x changeTag.sh"
                    sh "./changeTag.sh ${env.GIT_COMMIT}"
                    sh "kubectl apply -f main_app.yaml"
                }
            }
        }
    }
}
