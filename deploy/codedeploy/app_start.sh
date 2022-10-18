#!/bin/bash

REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone | sed s/.$//g)
AWS_ACCOUNT_ID=$(curl -s http://169.254.169.254/latest/dynamic/instance-identity/document | sed -nE 's/.*"accountId"\s*:\s*"(.*)".*/\1/p')
ECR_REPO_NAME=${$DEPLOYMENT_GROUP_NAME%"codedeploy"} # This name pattern is fixed from terraform
DOCKER_REPO_URL="$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO_NAME"
DOCKER_IMAGE_TAG="latest"

# Start the service
/usr/local/bin/docker-compose --env-file /pocket/strata-args.env -f /pocket/docker-compose.yml up -d
