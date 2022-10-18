#!/bin/bash

REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed s/.$//g)
AWS_ACCOUNT_ID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | sed -nE 's/.*"accountId"\s*:\s*"(.*)".*/\1/p')
ECR_REPO_NAME=${DEPLOYMENT_GROUP_NAME%"-codedeploy"} # This name pattern is fixed from terraform
DOCKER_REPO_URL="$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO_NAME"
DOCKER_IMAGE_TAG="latest"

# Docker login to ECR
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $DOCKER_REPO_URL

docker system prune -a -f 

# Docker pull the latest image
docker pull "$DOCKER_REPO_URL:$DOCKER_IMAGE_TAG"
