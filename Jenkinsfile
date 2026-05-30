pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 10'
                sh 'curl -f http://localhost:85/health'
            }
        }

        stage('Test API') {
            steps {
                sh '''
                curl -X POST http://localhost:85/api/tasks \
                  -H "Content-Type: application/json" \
                  -d '{"title":"jenkins test task"}'

                sleep 5

                curl http://localhost:85/api/tasks
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Pipeline failed. Check logs.'
        }
    }
}
