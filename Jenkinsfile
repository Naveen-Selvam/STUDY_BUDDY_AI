pipeline {
    agent any
    environment {
        DOCKER_HUB_REPO = "naveen583/studybuddy"
        DOCKER_HUB_CREDENTIALS_ID = "dockerhub-token"
    }
    stages {
        stage('Checkout Github') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/Naveen-Selvam/STUDY_BUDDY_AI.git']])
            }
        }        
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh 'sudo docker build -t ${DOCKER_HUB_REPO}:latest .'
                }
            }
        }
        stage('Push Image to DockerHub') {
            steps {
                echo 'Pushing Docker image to DockerHub...'
                script {
                    docker.withRegistry('https://registry.hub.docker.com', "${DOCKER_HUB_CREDENTIALS_ID}") {
                        dockerImage.push('latest')
                    }
                }
            }
        }
        // stage('Install Kubectl & ArgoCD CLI') {
        //     steps {
        //         echo 'Installing Kubectl and ArgoCD CLI...'
        //     }
        // }
        // stage('Apply Kubernetes & Sync App with ArgoCD') {
        //     steps {
        //         echo 'Applying Kubernetes and syncing with ArgoCD...'
        //     }
        // }
    }
} 