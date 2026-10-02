pipeline {

    agent any

    environment {
        IMAGE_NAME = "employee-api"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {

            steps {

                checkout scm

            }
        }
        stage('Check Tools') {
            steps {
                sh '''
                    export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

                    echo "PATH=$PATH"

                    echo "Docker:"
                    which docker
                    docker --version

                    echo "Kubectl:"
                    which kubectl
                    kubectl version --client

                    echo "Kubernetes:"
                    kubectl get nodes
                '''
            }
        }

        stage('Test') {

            steps {

                sh '''
                    python3 -m venv test-env

                    . test-env/bin/activate

                    pip install -r app/requirements.txt

                    python -m py_compile app/app.py

                    deactivate

                    rm -rf test-env
                '''
            }
        }

        stage('Build Docker Image') {

            steps {

                sh '''
                    docker build \
                    -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Deploy Flask') {

            steps {

                sh '''
                    kubectl apply \
                    -f k8s/flask-deployment.yaml

                    kubectl apply \
                    -f k8s/flask-service.yaml
                '''
            }
        }

        stage('Deploy Nginx') {

            steps {

                sh '''
                    kubectl apply \
                    -f k8s/nginx-configmap.yaml

                    kubectl apply \
                    -f k8s/nginx-html.yaml

                    kubectl apply \
                    -f k8s/nginx-deployment.yaml

                    kubectl apply \
                    -f k8s/nginx-service.yaml
                '''
            }
        }

        stage('Update Image') {

            steps {

                sh '''
                    kubectl set image \
                    deployment/flask-deployment \
                    flask=${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Verify Deployment') {

            steps {

                sh '''
                    kubectl rollout status \
                    deployment/flask-deployment \
                    --timeout=120s

                    kubectl rollout status \
                    deployment/nginx-deployment \
                    --timeout=120s

                    kubectl get pods

                    kubectl get services
                '''
            }
        }
    }
}