pipeline {
    agent any
    
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
            steps {
                sh '''
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Linting and Code Quality Checks') {
            steps {
                // Run linters and code quality checks
                sh "pylint data-engineering/src/"
            }
        }
    }

    /*post {
        always {
            sh ". ${VENV_DIR}/bin/deactivate"
        }
    }*/
}
