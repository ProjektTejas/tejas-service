from celery import Celery

celery_app: Celery = Celery("worker")

celery_app.conf.task_routes = {"tejas.worker.test_celery": "main-queue"}
celery_app.conf.update(task_track_started=True)
