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
                    docker info | grep Username
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

        stage('Verify Image') {
            steps {
                echo 'Verifying built image...'
                sh '''
                    docker images | grep "sashafefler/devops1114-flask"
                '''
            }
        }

        stage('Push to DH') {
            steps {
                echo 'Pushing the built image to Docker Hub with retry...'
                script {
                    def retries = 3
                    def success = false
                    while (!success && retries > 0) {
                        try {
                            sh '''
                                VERSION=$(cat "$WORKSPACE/$VERSION_FILE")
                                echo "Attempting to push: sashafefler/devops1114-flask:$VERSION"
                                docker push sashafefler/devops1114-flask:$VERSION
                            '''
                            success = true
                        } catch (Exception e) {
                            retries--
                            echo "Push failed. Retries left: ${retries}"
                            if (retries == 0) {
                                error "Docker push failed after multiple attempts."
                            }
                        }
                    }
                }
            }
        }

        stage('Run Container') {
            steps {
                echo "Ensuring that previous caontainers don't run, running the Docker container..."
                sh '''
                    docker stop devops1114-flask || true
                    docker rm devops1114-flask || true
                    docker run -d -p 8000:8000 --name devops1114-flask sashafefler/devops1114-flask:latest
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    echo "Checking if the app is running..."
                    if ! netstat -tuln | grep ":8000" > /dev/null 2>&1; then
                        echo "App is not running. Test cannot proceed."
                        exit 1
                    else
                        echo "App is running on port 8000. Proceeding with the test..."
                    fi
        
                    echo "Testing connectivity to 127.0.0.1..."
                    HTTP_STATUS_LOCAL=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000)
                    echo "Local HTTP status: $HTTP_STATUS_LOCAL"
        
                    echo "Testing connectivity to 192.168.1.26..."
                    HTTP_STATUS_EXTERNAL=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.1.26:8000)
                    echo "External HTTP status: $HTTP_STATUS_EXTERNAL"
        
                    if [ "$HTTP_STATUS_EXTERNAL" -ne 200 ]; then
                        echo "Test failed with HTTP status $HTTP_STATUS_EXTERNAL"
                        exit 1
                    else
                        echo "Test passed. HTTP status $HTTP_STATUS_EXTERNAL"
                    fi
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
