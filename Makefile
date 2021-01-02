build_image:
	docker build -t tejas .

run_docker:
	docker run -it --rm -v $(pwd)/requirements:/app/requirements --entrypoint /bin/bash tejas 

upload_req:
	scp -i "satyajit.pem" -r /mnt/d/Projects/ProjektTejas/tejas-service/requirements/ ubuntu@ec2-xx-xx-xx-xx.ap-south-1.compute.amazonaws.com:/home/ubuntu/
