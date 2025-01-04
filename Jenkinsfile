pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'sashafefler' // Your Docker Hub username
        DOCKER_PASSWORD = credentials('DH-token') // Docker Hub token stored in Jenkins credentials
        VERSION_FILE = 'version.txt'
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

        stage('Setup Versioning') {
            steps {
                echo 'Setting up versioning...'
                sh '''
                    if [ ! -f "$WORKSPACE/$VERSION_FILE" ]; then
                        echo "0.1" > "$WORKSPACE/$VERSION_FILE"
                        echo "Initialized versioning at 0.1"
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

        stage('Increment Version') {
            steps {
                echo 'Incrementing version...'
                sh '''
                    CURRENT_VERSION=$(cat "$WORKSPACE/$VERSION_FILE")
                    NEW_VERSION=$(echo "$CURRENT_VERSION" | awk -F. '{print $1 "." $2+1}')
                    echo "$NEW_VERSION" > "$WORKSPACE/$VERSION_FILE"
                    echo "Updated version to $NEW_VERSION"
                '''
            }
        }

        stage('Docker Login') {
            steps {
                echo 'Logging into Docker Hub...'
                sh '''
                    set -x # Log commands
                    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh '''
                    cd devops1114-flask
                    VERSION=$(cat "$WORKSPACE/$VERSION_FILE")
                    docker build -t sashafefler/devops1114-flask:$VERSION .
                    echo "Built Docker image with tag sashafefler/devops1114-flask:$VERSION"
                '''
            }
        }

        stage('Push to DH') {
            steps {
                echo 'Pushing the built image to Docker Hub...'
                sh '''
                    VERSION=$(cat "$WORKSPACE/$VERSION_FILE")
                    docker push sashafefler/devops1114-flask:$VERSION
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                sh '''
                    curl -s -o /dev/null -w "%{http_code}" http://$(hostname -I | awk '{print $1}'):8000 || echo "Test failed"
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploy'
            }
        }
    }
}
