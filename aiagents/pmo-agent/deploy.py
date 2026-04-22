"""PMO Agent Deployment Script."""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def deploy_local():
    """Deploy locally (already running)."""
    print("\n" + "=" * 80)
    print("LOCAL DEPLOYMENT")
    print("=" * 80)
    print("""
✅ PMO Agent is already running on http://localhost:8000

Available endpoints:
  📖 API Documentation: http://localhost:8000/docs
  🏥 Health Check: http://localhost:8000/health
  
  API Endpoints:
    POST /api/v1/change-request      - Generate Change Request
    POST /api/v1/project-plan        - Generate Project Plan
    POST /api/v1/raid-log            - Generate RAID Log
    POST /api/v1/full-analysis       - Run all agents

To stop the server: Press Ctrl+C

To start on different port:
  python -m uvicorn src.main:app --host 0.0.0.0 --port 9000

To run with auto-reload:
  python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
""")


def deploy_docker():
    """Deploy using Docker."""
    print("\n" + "=" * 80)
    print("DOCKER DEPLOYMENT")
    print("=" * 80)
    
    # Check if Docker is installed
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✓ Docker is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Docker is not installed")
        print("Install Docker from: https://www.docker.com/products/docker-desktop")
        return False
    
    print("""
Step 1: Build Docker image
  docker build -t pmo-agent:latest .

Step 2: Run Docker container
  docker run -p 8000:8000 \\
    -e OPENAI_API_KEY=sk-your-key-here \\
    pmo-agent:latest

Step 3: Access the application
  http://localhost:8000

Docker Compose (Easier):
  docker-compose up -d

To view logs:
  docker logs pmo-agent

To stop container:
  docker stop pmo-agent

To remove container:
  docker rm pmo-agent
  docker rmi pmo-agent:latest
""")
    
    print("\n🚀 To build and run now, execute:")
    print("  docker build -t pmo-agent:latest .")
    print("  docker run -p 8000:8000 pmo-agent:latest")


def deploy_aws():
    """Deploy to AWS."""
    print("\n" + "=" * 80)
    print("AWS DEPLOYMENT")
    print("=" * 80)
    print("""
Option 1: EC2 (Virtual Machine)
────────────────────────────────
1. Launch EC2 instance:
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (minimum)
   - Security group: Allow port 8000, 443

2. SSH into instance:
   ssh -i your-key.pem ubuntu@your-instance-ip

3. Install dependencies:
   sudo apt update && sudo apt install -y python3.11 pip git
   
4. Clone code and install:
   git clone your-repo.git pmo-agent
   cd pmo-agent
   pip install -r requirements.txt

5. Create systemd service:
   sudo nano /etc/systemd/system/pmo-agent.service
   
   [Unit]
   Description=PMO Agent API
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/pmo-agent
   ExecStart=/usr/bin/python3 -m uvicorn src.main:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target

6. Enable and start service:
   sudo systemctl enable pmo-agent
   sudo systemctl start pmo-agent
   sudo systemctl status pmo-agent

7. Setup reverse proxy (Nginx):
   sudo apt install -y nginx
   
   # Configure nginx to proxy port 8000

8. Setup SSL certificate (Let's Encrypt):
   sudo apt install -y certbot python3-certbot-nginx
   sudo certbot certonly --nginx -d your-domain.com

Cost: ~$10-30/month for t3.medium


Option 2: Elastic Beanstalk (Managed)
──────────────────────────────────────
1. Install EB CLI:
   pip install awsebcli

2. Initialize EB application:
   eb init -p python-3.11 pmo-agent

3. Create environment:
   eb create pmo-agent-env

4. Set environment variables:
   eb setenv OPENAI_API_KEY=sk-...

5. Deploy:
   eb deploy

6. Open in browser:
   eb open

Cost: ~$10-50/month depending on traffic


Option 3: ECS (Containers)
───────────────────────────
1. Build Docker image:
   docker build -t pmo-agent:latest .

2. Push to ECR:
   aws ecr get-login-password | docker login --username AWS --password-stdin YOUR_ECR_URI
   docker tag pmo-agent:latest YOUR_ECR_URI/pmo-agent:latest
   docker push YOUR_ECR_URI/pmo-agent:latest

3. Create ECS cluster and task definition

4. Launch service

Cost: ~$50-200+/month


Option 4: Lambda + API Gateway (Serverless)
──────────────────────────────────────────────
Perfect for low-traffic applications
Cost: Pay per request (very cheap!)

Requires code refactoring to run on Lambda
More complex setup but ultra-scalable


RECOMMENDED FOR MOST: EC2 + Nginx + Let's Encrypt
  ✓ Cost effective
  ✓ Full control
  ✓ Easy to manage
  ✓ Scalable
""")


def deploy_azure():
    """Deploy to Azure."""
    print("\n" + "=" * 80)
    print("AZURE DEPLOYMENT")
    print("=" * 80)
    print("""
Option 1: App Service
──────────────────────
1. Create resource group:
   az group create --name pmo-rg --location eastus

2. Create App Service plan:
   az appservice plan create --name pmo-plan --resource-group pmo-rg --sku B1 --is-linux

3. Create web app:
   az webapp create --resource-group pmo-rg --plan pmo-plan --name pmo-agent-app --runtime "python|3.11"

4. Deploy code:
   az webapp up --name pmo-agent-app --resource-group pmo-rg

5. Configure settings:
   az webapp config appsettings set --resource-group pmo-rg --name pmo-agent-app \\
     --settings OPENAI_API_KEY=sk-...

Cost: ~$50-100/month for B1 tier


Option 2: Container Instances
───────────────────────────────
Perfect for quick, simple deployments

1. Create container registry (ACR):
   az acr create --resource-group pmo-rg --name pmoacr --sku Basic

2. Build and push image:
   az acr build --registry pmoacr --image pmo-agent:latest .

3. Create container instance:
   az container create --resource-group pmo-rg --name pmo-agent \\
     --image pmoacr.azurecr.io/pmo-agent:latest \\
     --ports 8000 --cpu 1 --memory 1

Cost: Pay per second of execution (~$10-30/month)


RECOMMENDED: App Service for managed experience
""")


def deploy_gcp():
    """Deploy to Google Cloud Platform."""
    print("\n" + "=" * 80)
    print("GCP DEPLOYMENT")
    print("=" * 80)
    print("""
Option 1: Cloud Run (Recommended - Simplest)
──────────────────────────────────────────────
1. Install gcloud CLI:
   curl https://sdk.cloud.google.com | bash

2. Authenticate:
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID

3. Build and deploy:
   gcloud run deploy pmo-agent \\
     --source . \\
     --platform managed \\
     --region us-central1 \\
     --allow-unauthenticated

4. Set environment variables:
   gcloud run services update pmo-agent \\
     --set-env-vars OPENAI_API_KEY=sk-...

Cost: Pay per request (~$5-30/month for typical usage)


Option 2: Compute Engine (VM)
───────────────────────────────
Similar to AWS EC2

1. Create VM instance
2. SSH and install dependencies
3. Run application
4. Setup reverse proxy

Cost: ~$10-30/month


Option 3: App Engine
─────────────────────
Google's managed platform

1. Create app.yaml:
   runtime: python311
   env: standard

2. Deploy:
   gcloud app deploy

Cost: ~$10-50/month


RECOMMENDED: Cloud Run for easiest deployment
""")


def deploy_kubernetes():
    """Deploy to Kubernetes."""
    print("\n" + "=" * 80)
    print("KUBERNETES DEPLOYMENT")
    print("=" * 80)
    print("""
Prerequisites:
  - Kubernetes cluster (k3s, EKS, AKS, GKE)
  - kubectl installed
  - Harbor or DockerHub account

Step 1: Build and push Docker image
─────────────────────────────────────
  docker build -t your-registry/pmo-agent:latest .
  docker push your-registry/pmo-agent:latest


Step 2: Create Kubernetes manifests
──────────────────────────────────────
Create k8s/deployment.yaml:
  
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: pmo-agent
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: pmo-agent
    template:
      metadata:
        labels:
          app: pmo-agent
      spec:
        containers:
        - name: pmo-agent
          image: your-registry/pmo-agent:latest
          ports:
          - containerPort: 8000
          env:
          - name: OPENAI_API_KEY
            valueFrom:
              secretKeyRef:
                name: pmo-secrets
                key: openai-key
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10


Step 3: Create service
───────────────────────
Create k8s/service.yaml:
  
  apiVersion: v1
  kind: Service
  metadata:
    name: pmo-agent-service
  spec:
    type: LoadBalancer
    ports:
    - port: 80
      targetPort: 8000
    selector:
      app: pmo-agent


Step 4: Deploy
──────────────
  kubectl create secret generic pmo-secrets --from-literal=openai-key=sk-...
  kubectl apply -f k8s/
  kubectl get pods
  kubectl get svc


Step 5: Monitor
────────────────
  kubectl logs -f deployment/pmo-agent
  kubectl describe pod pmo-agent-XXXXX


Cost: Depends on cluster (usually $50-500+/month for managed K8s)


BENEFITS OF K8S:
  ✓ Enterprise-grade reliability
  ✓ Auto-scaling
  ✓ Self-healing
  ✓ Declarative deployments
  ✓ Easy A/B testing
  ✓ Multi-cloud ready
""")


def setup_monitoring():
    """Show monitoring setup."""
    print("\n" + "=" * 80)
    print("MONITORING & LOGGING")
    print("=" * 80)
    print("""
Recommended Monitoring Stack:
──────────────────────────────

1. Application Monitoring
   - Datadog: https://www.datadoghq.com (Recommended)
   - New Relic: https://newrelic.com
   - Prometheus + Grafana: Open source

2. Error Tracking
   - Sentry: https://sentry.io (Recommended)
   - Rollbar: https://rollbar.com
   - Bugsnag: https://www.bugsnag.com

3. Logging
   - CloudWatch (AWS)
   - Stackdriver (GCP)
   - Monitor (Azure)
   - Datadog Logs
   - Elasticsearch + Kibana (self-hosted)

4. Uptime Monitoring
   - Pingdom: https://www.pingdom.com
   - UptimeRobot: https://uptimerobot.com (Free tier available)
   - Datadog Synthetics

Setup Instructions for Sentry:
1. Create account at https://sentry.io
2. Create project (Python + FastAPI)
3. Add to requirements.txt: sentry-sdk[fastapi]
4. Add to main.py:
   
   import sentry_sdk
   sentry_sdk.init(
       dsn="your-sentry-dsn",
       traces_sample_rate=1.0
   )

Setup Instructions for Prometheus:
1. Install: pip install prometheus-client
2. Add to main.py:
   
   from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
   
   request_count = Counter('requests', 'Request count')
   request_duration = Histogram('request_duration_seconds', 'Request duration')

Setup Health Checks:
1. Already implemented at /health endpoint
2. Check status: curl http://localhost:8000/health
3. Setup with monitoring tool to alert if unhealthy
""")


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description="PMO Agent Deployment")
    parser.add_argument(
        "--option",
        choices=["local", "docker", "aws", "azure", "gcp", "kubernetes", "monitoring"],
        default="local",
        help="Deployment option"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 80)
    print("PMO AGENT - DEPLOYMENT GUIDE")
    print("=" * 80)
    
    if args.option == "local":
        deploy_local()
    elif args.option == "docker":
        deploy_docker()
    elif args.option == "aws":
        deploy_aws()
    elif args.option == "azure":
        deploy_azure()
    elif args.option == "gcp":
        deploy_gcp()
    elif args.option == "kubernetes":
        deploy_kubernetes()
    elif args.option == "monitoring":
        setup_monitoring()
    
    print("\n" + "=" * 80)
    print("✅ Deployment guide ready!")
    print("=" * 80)
    print("\nFor more information:")
    print("  📖 Read: DEPLOYMENT.md")
    print("  🔗 API Docs: http://localhost:8000/docs")
    print("  📞 Support: See README.md")


if __name__ == "__main__":
    main()
