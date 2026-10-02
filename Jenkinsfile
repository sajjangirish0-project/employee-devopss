pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
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

                    echo "===== DOCKER ====="
                    which docker
                    docker --version

                    echo "===== KUBECTL ====="
                    which kubectl
                    kubectl version --client

                    echo "===== KUBERNETES ====="
                    kubectl get nodes
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

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
                    export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

                    echo "Building Docker image..."

                    docker build \
                        -t ${IMAGE_NAME}:${IMAGE_TAG} .

                    echo "Docker image created:"
                    docker images | grep ${IMAGE_NAME}
                '''
            }
        }

        stage('Deploy Flask') {
            steps {
                sh '''
                    export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

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
                    export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

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
                    export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

                    kubectl set image \
                        deployment/flask-deployment \
                        flask=${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

                    echo "===== PODS ====="
                    kubectl get pods

                    echo "===== SERVICES ====="
                    kubectl get services

                    echo "===== FLASK ROLLOUT ====="
                    kubectl rollout status \
                        deployment/flask-deployment \
                        --timeout=120s

                    echo "===== NGINX ROLLOUT ====="
                    kubectl rollout status \
                        deployment/nginx-deployment \
                        --timeout=120s
                '''
            }
        }
    }
}