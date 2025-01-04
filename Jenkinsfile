pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'sashafefler' // Your Docker Hub username
        DOCKER_PASSWORD = credentials('DH-token') // Docker Hub token stored in Jenkins credentials
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
                    set -x # Log commands
                    echo "Username: $DOCKER_USERNAME"
                    echo "Password: $DOCKER_PASSWORD" # Masked in Jenkins logs
                    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    cd devops1114-flask
                    docker build -t sashafefler/devops1114-flask:latest .
                    echo "Running app on http://$(hostname -I | awk '{print $1}'):8000"
                '''
            }
        }

        stage('Push to DH') {
            steps {
                echo 'Pushing the built image to DockerHub'
                sh '''
                    docker push sashafefler/devops1114-flask:latest
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
