sudo docker rm -f ytenx
sudo docker run --detach --restart=always --name ytenx -p 127.0.0.1:7001:8000 ytenx
