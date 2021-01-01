from celery import Celery

celery_app = Celery("worker")

celery_app.conf.task_routes = {"tejas.worker.test_celery": "main-queue"}
