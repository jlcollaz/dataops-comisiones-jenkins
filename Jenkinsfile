pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t dataops-comisiones:latest .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'mkdir -p output'
                sh 'docker run --rm -v $WORKSPACE/output:/app/output dataops-comisiones:latest'
            }
        }

        stage('Validate Output') {
            steps {
                sh 'ls -lh output/'
                sh 'test -f output/comisiones_calculadas.xlsx'
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'output/*.xlsx', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Pipeline ejecutado correctamente. Artefacto Excel generado.'
        }
        failure {
            echo 'El pipeline falló. Revisar logs de Jenkins.'
        }
    }
}
