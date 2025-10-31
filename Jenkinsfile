pipeline {
    agent any

    environment {
        MYSQL_ROOT_PASSWORD = credentials('mysql-root-pass')
        MYSQL_DATABASE = credentials('mysql-db-name')
        DATABASE_URL = credentials('database-url')
        DOCKERHUB_USR = ''  // ⚠️ replace with your Docker Hub username
    }

    stages {

        stage('Checkout') {
            steps {
                echo '🌀 Fetching latest code from GitHub...'
                git branch: 'main',
                    url: ''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                sh '''
                    docker build -t ${DOCKERHUB_USR}/fastapi-app:latest .
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing image to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push ${DOCKERHUB_USR}/fastapi-app:latest
                    '''
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo '🚀 Deploying containers...'
                sh '''
                    echo "MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}" > .env
                    echo "MYSQL_DATABASE=${MYSQL_DATABASE}" >> .env
                    echo "DATABASE_URL=${DATABASE_URL}" >> .env

                    docker compose down
                    docker compose pull
                    docker compose up -d --force-recreate
                '''
            }
        }

    }

    post {
        success {
            echo '🎉 Deployment successful! FastAPI app is live!'
        }
        failure {
            echo '❌ Deployment failed. Check logs for details.'
        }
    }
}

