#!/bin/bash

# 1. Change directory to where Azure mounts your app code
cd /home/site/wwwroot

# 2. Download and extract portable Java JRE if it isn't already present
if [ ! -d "jdk-17.0.9+9-jre" ]; then
    echo "Downloading Java JRE..."
    curl -L -o jre.tar.gz https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jre_x64_linux_hotspot_17.0.9_9.tar.gz
    tar -xzf jre.tar.gz
    rm jre.tar.gz
    chmod +x jdk-17.0.9+9-jre/bin/java
fi

# 3. Activate the virtual environment packaged by GitHub Actions
source /home/site/wwwroot/antenv/bin/activate

# 4. Start the server
gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
