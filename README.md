# Tejas

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
- com.amazonaws.ap-south-1.lambda
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