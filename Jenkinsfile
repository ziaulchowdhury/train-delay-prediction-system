pipeline {
    // agent any
    agent {
        dockerfile { filename 'Dockerfile.build' }
    }

    environment {
        // Define environment variables
        PYTHON = 'python3'
        VENV_DIR = 'venv'
        DATA_DIR = 'data'
        MODEL_DIR = 'models'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout source code from your version control system (e.g., Git)
                checkout scm
                print("checked out code .......")
            }
        }

        stage('Setup') {
            agent {
                docker {
                    image 'python:3-alpine'
                }
            }
            steps {
                sh '''
                    ${PYTHON} -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
    }

    post {
        always {
            // Clean up steps
            sh "deactivate"
        }
    }
}
