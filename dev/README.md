# Development

```
docker run -it -v $(pwd)/requirements:/app/requirements --entrypoint /bin/bash tejas
```

```
pip install -r requirements.txt -t requirements
```

Instantiate an EC2 Instance, and add EC2's Security Group to the EFS inbound NFS rule

Mount the EFS by

```
sudo mount -t nfs4 -o nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport fs-341769e5.efs.ap-south-1.amazonaws.com:/ efs
```

Copy your stuff and unmount

```
sudo umount efs
```