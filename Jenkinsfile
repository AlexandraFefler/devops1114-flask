pipeline {
    agent any

    environment {
        DOCKER_USERNAME = 'shasatest' // Replace with your Docker Hub username
        DOCKER_PASSWORD = credentials('docker-hub-token') // Reference to Jenkins credentials
    }
    
    stages {
        stage('Cleanup') {
            steps {
                echo 'Cleaning up before cloning...'
                // Remove the repository folder if it exists
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
                echo 'Logging into Docker...'
                sh '''
                    echo "yes it is unsafe i know"
                    echo dckr_pat_pzbfRjsvDaGLZsfeXsL9x7e_-KU | docker login -u "shasatest" --password-stdin
                '''
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building...'
                sh '''
                    cd devops1114-flask
                    docker build -t devops1114-flask:latest .
                    echo "running app on http://$(hostname -I | awk '{print $1}'):8000"
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
