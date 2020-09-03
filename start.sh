sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker network prune -f
sudo docker volume rm $(sudo docker volume ls --filter dangling=true -q)

sudo docker network create mca-corp
sudo docker volume create webcode
sudo docker-compose up --build