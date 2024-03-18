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
    }

    post {
        always {
            // Clean up steps
            sh "deactivate" // Deactivate virtual environment
        }
    }
}
