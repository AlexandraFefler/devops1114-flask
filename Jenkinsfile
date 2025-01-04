pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'shasatest' // Your Docker Hub username
        DOCKER_PASSWORD = credentials('DH-shasatest') // Docker Hub token stored in Jenkins credentials
    }

    stages {
        stage('Ensure Docker Access') {
            steps {
                echo 'Ensuring Docker access...'
                sh '''
                    if ! docker info > /dev/null 2>&1; then
                        echo "Docker daemon not accessible. Ensure the Jenkins user is in the Docker group."
                        exit 1
                    else
                        echo "Docker is accessible."
                    fi
                '''
            }
        }

        stage('Cleanup') {
            steps {
                echo 'Cleaning up before cloning...'
                sh '''
                    if [ -d "devops1114-flask" ]; then
                        echo "Directory exists, cleaning up..."
                        rm -rf devops1114-flask
                    else
                        echo "Directory does not exist, no cleanup needed."
                    fi
                '''
            }
        }
        
        stage('Clone') {
            steps {
                echo 'Cloning git repo...'
                sh 'git clone https://github.com/AlexandraFefler/devops1114-flask.git'
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging into Docker Hub...'
                sh '''
                    set -x # Enable debug mode to log each command
                echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                if [ $? -ne 0 ]; then
                    echo "Docker login failed. Check Docker Hub credentials or permissions."
                    exit 1
                else
                    echo "Docker login succeeded."
                fi
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    cd devops1114-flask
                    docker build -t devops1114-flask:latest .
                    echo "Running app on http://$(hostname -I | awk '{print $1}'):8000"
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Test'
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploy'
            }
        }
    }
}
