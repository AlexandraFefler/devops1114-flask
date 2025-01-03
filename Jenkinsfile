pipeline {
    agent any

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
        
        stage('Build') {
            steps {
                echo 'Build'
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
