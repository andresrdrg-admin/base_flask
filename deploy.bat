cls
@echo off
SET mypath=%~dp0
FOR /f %%i IN ('docker ps -qf "name=^---NAME-APPLICATION---_cont"') DO SET containerId=%%i

IF NOT "%containerId%" == "" (
    docker rm -f -v "%containerId%"
)

docker image remove ---NAME-APPLICATION---
docker build -t ---NAME-APPLICATION---:latest .
docker run -dit --restart unless-stopped -p 5000:5000 --volume "%mypath:~0,-1%\:/app" --name ---NAME-APPLICATION---_cont ---NAME-APPLICATION---:latest