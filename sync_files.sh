#!/bin/bash

rsync -avz Dockerfile docker-compose.yml .env requirements.txt src \
--exclude src/__pycache__/ \
-e "ssh -i ~/.ssh/t490_key.pem" \
ubuntu@18.199.129.189:/home/ubuntu/recipe_bot
