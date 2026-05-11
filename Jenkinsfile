pipeline {
    agent { label 'agent2' }

    environment {
        IMAGE_NAME = "shivanhussain/todo-remember-app:latest"
        REPORT_DIR = "trivy-reports"
        EMAIL_ID = "Your-email-address"
    }

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                url: 'https://github.com/ShivanHussain/Todo_Rememeber.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --no-cache -t todo-remember .'
            }
        }

        stage('Trivy Scan') {
            steps {
                sh '''
                    mkdir -p ${REPORT_DIR}

                    echo "Running Trivy Scan..."

                    trivy image \
                    --severity HIGH,CRITICAL \
                    --format table \
                    -o ${REPORT_DIR}/trivy-report-${BUILD_NUMBER}.txt \
                    todo-remember
                '''
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag todo-remember ${IMAGE_NAME}'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker compose down || true
                    docker compose up -d
                '''
            }
        }
    }

   post {

    success {

        emailext(
            subject: "SUCCESS: Jenkins Build ${env.BUILD_NUMBER}",

            body: """
                Build Successful!

                Job Name: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}

                Docker image built successfully.
                Trivy scan completed.

                Console log and Trivy report attached.
            """,

            to: "${env.EMAIL_ID}",
            attachLog: true,
            attachmentsPattern: "trivy-reports/trivy-report-${BUILD_NUMBER}.txt"
        )

        echo "Pipeline Succeeded!"
    }

    failure {

        emailext(
            subject: "FAILED: Jenkins Build ${env.BUILD_NUMBER}",

            body: """
                Build Failed!

                Job Name: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}

                Pipeline execution failed.
                Check attached console log and Trivy report.
            """,

            to: "${env.EMAIL_ID}",
            attachLog: true,
            attachmentsPattern: "trivy-reports/trivy-report-${BUILD_NUMBER}.txt"
        )

        echo "Pipeline Failed!"
    }
}
}