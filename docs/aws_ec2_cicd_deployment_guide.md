# AWS EC2 Container Deployment & CI/CD Pipeline Guide

This guide provides step-by-step instructions for creating an **AWS EC2 instance**, containerizing your FastAPI application, and configuring an automated **GitHub Actions CI/CD deployment pipeline**. It also explains exactly what happens during successful deployments versus various test and build failure scenarios.

---

## 🏗️ Architecture Overview

```mermaid
flowchart TD
    subgraph Local Environment
        Dev[Developer] -->|git push origin main| GH[GitHub Repository]
    end

    subgraph GitHub Actions Cloud Runner
        GH -->|Triggers Workflow| CI[Continuous Integration Job]
        CI --> Step1[1. Checkout Code]
        CI --> Step2[2. Set up Python 3.12]
        CI --> Step3[3. Install Dependencies]
        CI --> Step4[4. Run Pytest Suite - 25 Tests]
        
        Step4 -->|Tests Pass ✅| CD[Continuous Deployment Job]
        Step4 -->|Tests Fail ❌| Stop[STOP Pipeline! Deployment Blocked ⛔]
    end

    subgraph AWS EC2 Server
        CD -->|SSH Connection| EC2[EC2 Instance - Ubuntu]
        EC2 --> Pull[Git Pull / Docker Pull]
        EC2 --> Build[Docker Build - t python-api]
        EC2 --> Run[Docker Run - p 8000:8000]
        Run --> App[FastAPI Application Live on Port 8000 🎉]
    end
```

---

## Part 1: Setting Up the AWS EC2 Instance

### 1. Launch an EC2 Instance
1. Log in to the **AWS Management Console** and navigate to **EC2**.
2. Click **Launch Instance**.
3. Name your instance: `python-fastapi-server`.
4. Choose **OS Image**: Select **Ubuntu Server 24.04 LTS (64-bit x86)**.
5. Instance Type: Select **`t2.micro`** (Free Tier eligible) or `t3.micro`.
6. **Key Pair**: Click *Create new key pair* (e.g. `fastapi-ec2-key.pem`), download it, and store it securely on your computer.

### 2. Configure Security Group (Firewall Rules)
In Network Settings, configure inbound rules to allow traffic:

| Type | Protocol | Port Range | Source | Description |
| :--- | :--- | :--- | :--- | :--- |
| **SSH** | TCP | `22` | My IP or Anywhere (`0.0.0.0/0`) | Remote SSH terminal access |
| **HTTP** | TCP | `80` | Anywhere (`0.0.0.0/0`) | Standard web traffic |
| **Custom TCP** | TCP | `8000` | Anywhere (`0.0.0.0/0`) | FastAPI Application Port |

Click **Launch Instance**.

---

### 3. Connect to EC2 & Install Docker
Open your terminal (PowerShell or Bash) and connect to your EC2 instance using your `.pem` key:

```bash
# 1. Set key permissions (Linux/Mac only: chmod 400 fastapi-ec2-key.pem)
ssh -i "fastapi-ec2-key.pem" ubuntu@<YOUR_EC2_PUBLIC_IP>
```

Once connected inside your EC2 server, install Docker and Git:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io git

# Start Docker service and enable on boot
sudo systemctl start docker
sudo systemctl enable docker

# Allow 'ubuntu' user to run Docker commands without sudo
sudo usermod -aG docker ubuntu

# Apply group permissions (or log out & log back in)
newgrp docker

# Verify Docker installation
docker --version
```

---

## Part 2: Configuring GitHub Actions Secrets

To allow GitHub Actions to securely log into your EC2 instance over SSH without exposing passwords or keys:

1. Open your GitHub Repository in your browser: `https://github.com/saikumar005/python-pytest-cicd-demo`.
2. Go to **Settings** → **Secrets and variables** → **Actions**.
3. Click **New repository secret** and add the following 3 secrets:

| Secret Name | Value Example | Description |
| :--- | :--- | :--- |
| **`EC2_HOST`** | `54.210.12.34` | Public IPv4 Address of your EC2 instance |
| **`EC2_USERNAME`** | `ubuntu` | Default SSH username for Ubuntu instances |
| **`EC2_SSH_KEY`** | `-----BEGIN RSA PRIVATE KEY-----...` | Contents of your downloaded `fastapi-ec2-key.pem` file |

---

## Part 3: Complete CI/CD Pipeline Workflow

Update your [.github/workflows/ci.yml](file:///d:/3%20months%20plan/python_testing/.github/workflows/ci.yml) file to include both **Testing (CI)** and **Deployment to EC2 (CD)** stages:

```yaml
name: CI/CD Pipeline to AWS EC2

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  # ==========================================
  # JOB 1: CONTINUOUS INTEGRATION (CI)
  # ==========================================
  test:
    name: Run Pytest Suite & Code Checks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Pytest Suite (Unit & Integration Tests)
        run: |
          pytest -v

  # ==========================================
  # JOB 2: CONTINUOUS DEPLOYMENT (CD)
  # Runs ONLY if 'test' job completes successfully!
  # ==========================================
  deploy:
    name: Deploy Container to AWS EC2
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest

    steps:
      - name: SSH into EC2 and Deploy Application
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            echo "1. Pulling latest code from GitHub main branch..."
            if [ ! -d "python_testing" ]; then
              git clone https://github.com/saikumar005/python-pytest-cicd-demo.git python_testing
              cd python_testing
            else
              cd python_testing
              git fetch origin main
              git reset --hard origin/main
            fi

            echo "2. Building Docker Image..."
            docker build -t fastapi-app:latest .

            echo "3. Stopping and Removing old running container (if any)..."
            docker stop fastapi-container || true
            docker rm fastapi-container || true

            echo "4. Running new Docker Container..."
            docker run -d --name fastapi-container -p 8000:8000 --restart always fastapi-app:latest

            echo "5. Verifying running container status..."
            docker ps
```

---

## 🔬 Part 4: Scenario Analysis - How CI/CD Behaves in All Conditions

### Scenario 1: All Tests PASS (Successful CI/CD Deployment) ✅

```text
[git push origin main] 
       ↓
CI Job Starts on GitHub Runner:
  1. Installs Python 3.12 & requirements.txt
  2. Runs `pytest -v` (25 tests collected)
  3. Result: 25 PASSED in 0.58s
       ↓
CD Job Triggered automatically:
  1. GitHub SSHs into your AWS EC2 instance.
  2. EC2 pulls latest commit (`git reset --hard origin/main`).
  3. EC2 builds fresh Docker image (`docker build -t fastapi-app`).
  4. EC2 stops old container and launches new container (`docker run -d -p 8000:8000`).
       ↓
Result: App updated seamlessly on http://<EC2_PUBLIC_IP>:8000/health with 0 downtime!
```

---

### Scenario 2: Unit or Integration Test FAILS (Deployment Blocked) ❌

**What happens if someone introduces a bug (e.g. `divide(10, 0)` returns `0` instead of raising `ValueError`)?**

```text
[git push origin main]
       ↓
CI Job Starts:
  1. Pytest executes test suite.
  2. `test_divide_by_zero` fails assertion:
     E  Failed: DID NOT RAISE <class 'ValueError'>
       ↓
Pytest exits with Exit Code 1.
       ↓
CI Job Status: FAILED (Red X mark on GitHub UI)
       ↓
CD Job: CANCELLED / SKIPPED (`needs: test` requirement failed!)
       ↓
Result on EC2:
  - GitHub NEVER connects to your EC2 instance.
  - The live application on EC2 continues running the PREVIOUS stable Docker container!
  - Production users are NEVER exposed to the broken code.
```

---

### Scenario 3: Syntax Error or Broken Dependencies (Build Failure) 💥

**What happens if someone misspells an import like `from fastapiii import FastAPI` or breaks `requirements.txt`?**

```text
[git push origin main]
       ↓
CI Job Starts:
  1. Runner attempts `pip install -r requirements.txt` or `pytest`.
  2. Python throws `ModuleNotFoundError: No module named 'fastapiii'`.
       ↓
Command fails with exit code non-zero.
       ↓
CI Job Status: FAILED
CD Job: SKIPPED
       ↓
Result: Developer gets email notification / Slack alert of pipeline failure. EC2 remains 100% stable.
```

---

### Scenario 4: SSH / EC2 Server Down (Deployment Failure) 📡

**What happens if all 25 unit tests pass, but your EC2 instance is turned off or Security Group blocks SSH?**

```text
CI Job: PASSED (25 tests passed) ✅
       ↓
CD Job Starts:
  1. GitHub Actions attempts `appleboy/ssh-action` connection to secrets.EC2_HOST.
  2. Connection times out after 30 seconds (Port 22 unreachable / instance stopped).
       ↓
CD Job Status: FAILED (Red X on CD step)
       ↓
Result: You know your code is correct (tests passed), but deployment infrastructure needs attention.
```

---

### Scenario 5: Docker Container Runtime Crash (Post-Deployment Health Fail) 🩺

**What happens if Docker builds, but the container crashes upon launching (e.g. missing environment variable)?**

```text
CI Job: PASSED ✅
CD Job SSH connection: SUCCESSFUL ✅
Docker Build: SUCCESSFUL ✅
Docker Run: Launches container
       ↓
Post-Deployment Check (optional step in workflow):
  `curl --fail http://localhost:8000/health`
       ↓
If container crashed on start, `curl` returns exit code 7 (Failed to connect).
CD Job flags status as FAILED!
```

---

## Part 5: Testing Your Live EC2 Deployment

Once deployed, test your endpoints from anywhere in the world using `curl` or your browser:

### 1. Health Check Endpoint
```bash
curl http://<YOUR_EC2_PUBLIC_IP>:8000/health
```
**Response:**
```json
{
  "status": "ok",
  "app": "python-testing"
}
```

### 2. Calculation Endpoint
```bash
curl -X POST "http://<YOUR_EC2_PUBLIC_IP>:8000/calculate" \
     -H "Content-Type: application/json" \
     -d '{"operation": "add", "a": 25, "b": 75}'
```
**Response:**
```json
{
  "operation": "add",
  "result": 100.0
}
```

---

## Summary Matrix of Pipeline Behaviors

| Event | Pytest Status | GitHub Actions CI | EC2 Deployment (CD) | Live EC2 App Status |
| :--- | :--- | :--- | :--- | :--- |
| **All Tests Pass** | 25 Passed ✅ | SUCCESS 🟢 | EXECUTED 🟢 | Updated to new code automatically |
| **Unit Test Fails** | 1 Failed ❌ | FAILED 🔴 | **BLOCKED (Skipped) ⛔** | Runs previous stable version |
| **Syntax Error** | Collection Error ❌ | FAILED 🔴 | **BLOCKED (Skipped) ⛔** | Runs previous stable version |
| **EC2 Server Offline** | 25 Passed ✅ | SUCCESS 🟢 | FAILED 🔴 | Remains on previous state until server recovers |
