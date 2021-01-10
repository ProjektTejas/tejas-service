<h1 align="center">Tejas.AI 🔥- Tejas Service</h1>

---

<div align="center">
<img src="logo/logo-whitemdpi.png" >
</div>

> Tejas (तेजस) means brain, flame, glow, radiance (just like my models :p)

---

This repository contains the main backend which handles the API Requests, it uses FastAPI and Mangum ASGI Handler. Once train_model is invoked, it stores the dataset in S3, which invokes the training lambda. This service also gives the user ability to query status of training, downloading models and also perform inferencing.

![maintainer](https://img.shields.io/badge/maintainer-shadowleaf-blue)
![GitHub stars](https://img.shields.io/github/stars/ProjektTejas/tejas-ml-service?style=social)

## Deployed Website: [http://tejas.tensorclan.tech/](http://tejas.tensorclan.tech/) or [https://project-tejas-web.vercel.app/](https://project-tejas-web.vercel.app/)

## Docs Website: [https://projekt-tejas-docs.vercel.app/](https://projekt-tejas-docs.vercel.app/)

## Demo

![demo](tejas-demo.gif)

## Deployment

EFS must have this structure, and should be mounted to `/mnt/tejas-fs` in Lambda

```text
- tejas-libs
- tejas-models
- tejas-pretrained
- tejas-datasets
```

VPC Endpoints are essential for this project to work, make sure to enable the following Endpoints with Appropriate Security Groups and Routing Table

```text
- com.amazonaws.ap-south-1.dynamodb
- com.amazonaws.ap-south-1.lambda # not needed, this incurred me costs, since this is a ENI
- com.amazonaws.ap-south-1.s3
```

NOTE: You will be charged for the Endpoints, plan accordingly (Use minimum Availability Zone for Lower Costs)

Download these models into `tejas-pretrained`

 ```shell script
 wget https://download.pytorch.org/models/mobilenet_v2-b0353104.pth
 ```

## Notes

- sometimes port `8000` does not work in WSL, so instead use `5000`
- `uvicorn tejas.main:app --host=0.0.0.0 --port=5000`

---

<h3 align="center">Made with 💘 by Satyajit Ghana</h3>
