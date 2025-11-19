ssh -i itsdcopilot.pem ec2-user@13.126.145.0

sudo systemctl start docker

sudo systemctl enable docker

sudo usermod -a -G docker ec2-user