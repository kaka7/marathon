Sudo gpasswd -a user docker

Top
Logs -f
Stop start restart
docker run -device


bethgelab/deeplearning:cuda9.0-cudnn7


传文件 curl localhost:8000/api/v1/upimg -F "file=@/Users/fungleo/Downloads/401.png" -H "token: 222" -v
传参数 curl localhost:9999/api/daizhige/article -X POST -H "Content-Type:application/json" -d '"title":"comewords","content":"articleContent"'

docker save imagename >/filename.tar (-o .tar image)
docker save -o 镜像名称
docker export -o 容器名称

Ctrl+P+Q进行退出容器

docker load < /filename.tar(-i .tar)
docker ps -all
 /var/lib/docker

docker commit hashcode imgeID
docker ps -a -q | xargs -i docker rm -f {}

dockerfile
FROM ubuntu:16.04
MAINTAINER
RUN echo hello
    /bin/sh -c command
RUN ["/bin/sh","-c","echo hello"]
expose 80
docker run -p 80 -d dor/test nginx -g "daemon off;"

 docker images --filter "dangling=true" -q

docker run -i -t ubuntu:16.04 /bin/bash

docker commit <容器id> 新的镜像名
docker run  -v /Users/zjl/python3i/py3image:/py3image  -w /py3image ubuntu python3 a.py
docker run -v /Users/zjl/python3i/py3image:/py3image -w /py3image ubuntu pip3 install -r requirements.txt


docker inspect -f '{{.ID}}' python
docker cp 本地路径 容器长ID:容器路径 
docker cp /home/naruto/Downloads/anaconda2 22bbb1895bf8265fbe6d5f3c398f5845a6458f86bc69810872f35460d6c6937c:/appcom/

docker exec -it cf432343b31b /bin/bash
docker attach CONTAINER_ID重新连接进容器
docker run -itd ubuntu:16.04 /bin/bash
docker run -it -v /test:/soft centos /bin/bash 所谓的相对路径指的是/var/lib/docker/volumes/ 绝对路径

Dockerfile要注意的点

    用&&\把所有命令串起来在一个Run里执行，避免产生太多层
    可以把/etc/apt/sources.list拷过去，加速apt-get install; 把pip.conf拷到/root/.config/pip/pip.conf，指向douban的源，加速pip install
    所有安装都是silent mode, 包括: apt-get -y、anaconda -b等
    报pip not found: anaconda不会自动把bin加入PATH，需要手工加：ENV PATH /root/anaconda2/bin:$PATH
    每个阶段的命令写在一起，从COPY+ENV+RUN，这样万一下面的COPY改了，还能重用以前的cache
    COPY要这么写：COPY ta-lib /tmp/ta-lib，如果只是COPY ta-lib /tmp/只会把ta-lib里面的内容拷过去
    国内的镜像源有时apt-get install的时候会报"Hash Sum mismatch"的错误，不覆盖/etc/apt/sources.list，用官方的就好
    很多server比如nginx、jupyter都默认监听localhost，要改成0.0.0.0，才能在容器外访问

build + export image

docker build -t test:v0.1 . dockerfile创建镜像
docker run -i -p 8686:8686 test:v0.1
docker save test:v0.1 | gzip > portfolio.tar.zip
//复制到其他机器上，导入
docker load -i portfolio.tar.zip

/etc/docker/daemon.json 

docker run -d -p 22 -p 80:8080 python_ubuntu /usr/sbin/sshd -D

docker容器内python执行flask程序：
修改flask的host=‘0.0.0.0’
命令：
docker run -p 5001:5000 -v /Users/zjl/Desktop/aaa/spider:/py3image  -w /py3image python3env python runflask.py

nvidia-docker run --rm nvidia/cuda nvidia-smi

echo 'alias docker=nvidia-docker' >> ~/.bashrc

DOCKER_OPTS="--graph=/home/docker"

sudo nvidia-docker info
nvidia-docker run --rm nvidia/cuda:8.0-devel nvidia-smi
$ nvidia-docker run --rm nvidia/cuda:8.0 nvidia-smi


nvidia-docker plugin failed.网上查不到解决办法
sudo apt install nvidia-modprobe

systemctl daemon-reload
service docker restart

docker run --rm -u $(id -u):$(id -g) -v $(pwd):$(pwd) -w $(pwd) bvlc/caffe:gpu caffe train --solver=example_solver.prototxt

/etc/docker/daemon.json

https://github.com/NVIDIA/nvidia-docker
--rm        退出容器清除数据

下面这个‘docker run’命令会映射新安装的GPU设备到TensorFlow容器中。详细命令如下：
$ docker run --device /dev/nvidia0:/dev/nvidia0 --device /dev/nvidia1:/dev/nvidia1 --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-uvm:/dev/nvidia-uvm -it -p 8888:8888 –privileged tflowgpu
例如，下面这个命令会将当前目录映射到docker容器，并且调用CUDA库来完成jpeg的编解码任务。详细命令如下：
sudo nvidia-docker run -v /home/gtx/work/huangxing/cuda/samples/7_CUDALibraries/jpegNPP:/outdata nvidia/cuda bash -c  "cd /outdata;./jpegNPP -input=data/Growth_of_cubic_bacteria_25x16.jpg -output=output.jpg"
cd /home/gtx/work/huangxing/cuda/samples/7_CUDALibraries/jpegNPP
sudo nvidia-docker run -v /home/gtx/work/huangxing/cuda/samples/7_CUDALibraries/jpegNPP:/outdata nvidia/cuda bash -c  "cd /outdata;./test.sh"
6.常用命令
sudo docker rm $(sudo docker ps -a -q) //删掉所有的container
sudo docker run -it ubuntu su - root bash -c “/usr/bin/X :0”
sudo docker run -v /home/gtx/work/huangxing:/outdata bash -c “/usr/bin/X :0”
sudo docker run ubuntu /bin/echo 'hellow'
sudo docker run -it ubuntu su - root bash -c /bin/bash
sudo nvidia-docker run -it -v /usr/bin/X:/outdata/X nvidia/cuda su - root -c '/bin/sh'
sudo nvidia-docker run -it -v /usr/lib/xorg/Xorg:/outdata/ Xorg nvidia/cuda su - root -c '/bin/sh'


从镜像中生成容器：
sudo nvidia-docker run -p 5200:5000 -v /home/knight/dockerTest/Features:/CCF_FaceRecog/datasets/Features -v /home/knight/dockerTest/ini:/CCF_FaceRecog/datasets/ini -v /home/knight/dockerTest/Upload:/CCF_FaceRecog/datasets/UploadImages –restart=always ccf_facerecognition:latest python manage_server.py

-p 端口映射，宿主机端口：开放的容器端口
-v 路径映射，宿主机路径：容器路径
–restart=always 开机自启
ccf_facerecognition:latest 镜像名称
python manage_server.py 运行该py文件，这样写需要在Dockerfile的最后写成：

RUN mkdir -p /CCF_FaceRecog
WORKDIR /CCF_FaceRecog
COPY . /CCF_FaceRecog
CMD [“/bin/bash”]

而manage_server.py文件就放在容器中的/CCF_FaceRecog文件夹下。

如果Dockerfile的最后写成了：

CMD [“python”, “index.py”]
则启动容器后会自动执行index.py文件。

Dockerfile中要使用ENV PATH /opt/conda/bin:$PATH 指定通过anaconda安装的python的环境变量

docker logs containername<containerid>

docker build
docker build -t nginx:1.6 .

netstat -anplt | grep 80

 docker run automation/toolbox --workers 5




nvidia-docker run -itd -v ~/Documents/writing/:/data  wjb2:latest

docker run -i -t --name test111 -v 本机:容器内 -p 3000:3000 -p 18888:18888 --privileged=true node-mongo0901 sh -c 'service mongod start && npm run start'


# docker run -i -t image /bin/bash ./home/start.sh

docker run -idt ***/*** /bin/bash cs1.sh； cs2.sh； cs3.sh
最好在每个脚本后面都加上 tail -f /dev/null

sudo docker exec myContainer bash -c "cd /home/myuser/myproject && git fetch ssh://gerrit_server:29418/myparent/myproject ${GERRIT_REFSPEC} && git checkout FETCH_HEAD";
sudo docker exec myContainer bash -c "cd /home/myuser/myproject;git fetch ssh://gerrit_server:29418/myparent/myproject ${GERRIT_REFSPEC};git checkout FETCH_HEAD";

[root@docker-test ~]# docker run -ti -d --name my-nginx6 -p 192.168.10.214:8077:80/udp docker.io/nginx 

container内部访问web服务

$ curl http://localhost

docker pull 

docker tag tf17:v2.4 hub.io/traffic/tf17:v2.4
docker push hub.io/traffic/tf17:v2.4

执行如下命令从container内部退出。

Ctrl+ p, Ctrl+q


从container外部访问docker container内部的web服务

$ curl http://localhost:8080
$ curl http://localhost:8080


https://github.com/cheerss/deep-docker/tree/9.0-cudnn7-devel-ubuntu16.04) (branch 9.0-cudnn7-devel-ubuntu16.04)

https://hub.docker.com/r/cheerss/deep-docker 直接网页查看
docker pull cheerss/deep-docker:9.0-cudnn7-devel-ubuntu16.04


    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
    docker ps -a

    
docker inspect --format='{{.Id}} {{.Parent}}' $(docker images --filter since=9ac2c59b808f --quiet)
docker rmi souyunku/nginx:v1




-e username='cat' 	设置环境变量



opencv docker
# OpenCV 3.4.2
#
# Dependencies
RUN apt-get install -y --no-install-recommends \
    libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libgtk2.0-dev \
    liblapacke-dev checkinstall
# Get source from github
RUN git clone -b 3.4.2 --depth 1 https://github.com/opencv/opencv.git /usr/local/src/opencv

#这里自己先离线下载对应版本后做如下处理
# Compile
RUN cd /usr/local/src/opencv && mkdir build && cd build && \
    cmake -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D BUILD_TESTS=OFF \
          -D BUILD_PERF_TESTS=OFF \
          -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
          .. && \
    make -j"$(nproc)" && \
    make install
