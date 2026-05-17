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
                sh '''
                    rm -rf output
                    mkdir -p output

                    docker rm -f dataops-comisiones-run || true
                    docker create --name dataops-comisiones-run dataops-comisiones:latest
                    docker start -a dataops-comisiones-run
                    docker cp dataops-comisiones-run:/app/output/comisiones_calculadas.xlsx output/comisiones_calculadas.xlsx
                    docker rm dataops-comisiones-run
                '''
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
            echo 'Pipeline ejecutado correctamente. Artefacto Excel generado y archivado.'
        }
        failure {
            echo 'El pipeline falló. Revisar logs de Jenkins.'
        }
    }
}
