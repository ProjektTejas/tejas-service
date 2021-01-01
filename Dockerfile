# since this will be deployed to lambda
FROM lambci/lambda:build-python3.8

# this is just for local testing
RUN pip install uvicorn
EXPOSE 8000

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "uvicorn", "tejas.main:app", "--host", "0.0.0.0", "--port", "8000"]
