pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'sashafefler' // Your Docker Hub username
        DOCKER_PASSWORD = credentials('DH-token') // Docker Hub token stored in Jenkins credentials
        VERSION_FILE = 'version.txt'
        EC2_HOST = '54.242.104.130' // Replace with your EC2's public IP or DNS
    }

    stages {
            //             WAS FOR DEBUG             //
        // stage('Ensure Docker Access') {
        //     steps {
        //         echo 'Ensuring Docker access...'
        //         sh '''
        //             if ! docker info > /dev/null 2>&1; then
        //                 echo "Docker daemon not accessible. Ensure the Jenkins user is in the Docker group."
        //                 exit 1
        //             else
        //                 echo "Docker is accessible."
        //             fi
        //         '''
        //     }
        // }

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

            //             WAS FOR DEBUG             //
        // stage('Verify Image') {
        //     steps {
        //         echo 'Verifying built image...'
        //         sh '''
        //             docker images | grep "sashafefler/devops1114-flask"
        //         '''
        //     }
        // }

    // add tag "latest" in addition to version 
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
                echo "Ensuring that previous containers don't run, running the Docker container..."
                sh '''
                    VERSION=$(cat "$WORKSPACE/$VERSION_FILE")
                    docker stop devops1114-flask || true
                    docker rm devops1114-flask || true
                    docker run -d -p 8000:8000 --name devops1114-flask sashafefler/devops1114-flask:$VERSION
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    sleep 5
                    if curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000 | grep -q "^200$"; then
                        echo "Test passed: App is responding with HTTP 200."
                    else
                        echo "Test failed: App is not responding with HTTP 200."
                        exit 1
                    fi
                '''
            }
        }

        // ssh -o StrictHostKeyChecking=no -> automatic 'yes' response to asking to confirm trusting the server we try to connect to 
        // <<EOF commands...EOF executes all the commands inside here in the ssh command (inside the connected machine) so we don't have to use ssh for every command 
        // docker stop devops1114-flask || true -> try to stop a running container, but if such container doesn't exist and the command fails, then return true anyway cuz we got to the state we wanted which is "no such container running" 
        stage('Deploy') {
            steps {
                echo 'Deploying to EC2 instance...'
                withCredentials([sshUserPrivateKey(credentialsId: 'ec2-key', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        VERSION=$(cat "$WORKSPACE/$VERSION_FILE")
                        chmod 400 $SSH_KEY
                        echo "Connecting to EC2 instance..."
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@$EC2_HOST <<EOF
                        echo "Stopping existing container (if any)..."
                        docker stop devops1114-flask || true
                        docker rm devops1114-flask || true

                        echo "Pulling latest Docker image..."
                        docker pull sashafefler/devops1114-flask:$VERSION

                        echo "Running the new container..."
                        docker run -d -p 8000:8000 --name devops1114-flask sashafefler/devops1114-flask:$VERSION

                        echo "Deployment completed!"EOF
                    '''
                }
            }
        }
    }
}
