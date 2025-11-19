@echo off
echo 🚀 Setting up ITSD Copilot on EC2...
echo.

set EC2_IP=13.126.145.0
set KEY_FILE=itsdcopilot.pem

echo Step 1: Creating directories on EC2...
ssh -i %KEY_FILE% ec2-user@%EC2_IP% "mkdir -p /home/ec2-user/itsd-copilot/backend"
ssh -i %KEY_FILE% ec2-user@%EC2_IP% "mkdir -p /home/ec2-user/itsd-copilot/frontend"
ssh -i %KEY_FILE% ec2-user@%EC2_IP% "mkdir -p /home/ec2-user/itsd-copilot/knowledge_base"

echo Step 2: Uploading backend files...
scp -i %KEY_FILE% -r backend\* ec2-user@%EC2_IP%:/home/ec2-user/itsd-copilot/backend/

echo Step 3: Uploading frontend files...
scp -i %KEY_FILE% -r frontend\* ec2-user@%EC2_IP%:/home/ec2-user/itsd-copilot/frontend/

echo Step 4: Uploading knowledge base...
scp -i %KEY_FILE% -r knowledge_base\* ec2-user@%EC2_IP%:/home/ec2-user/itsd-copilot/knowledge_base/

echo Step 5: Uploading docker-compose...
scp -i %KEY_FILE% docker-compose.yml ec2-user@%EC2_IP%:/home/ec2-user/itsd-copilot/

echo.
echo ✅ Upload complete!
echo.
echo 📝 Next steps:
echo 1. Run deployment on EC2: 
echo    ssh -i itsdcopilot.pem ec2-user@13.126.145.0
echo    cd /home/ec2-user/itsd-copilot
echo    docker-compose up --build -d
echo.
pause