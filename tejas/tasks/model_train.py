import traceback

from tejas.core.celery_app import celery_app

from celery import states


@celery_app.task(name="model_train.task", bind=True)
def model_train(self):
    try:
        # train the model here
        pass
    except Exception as ex:
        self.update_state(
            state=states.FAILURE,
            meta={
                "exc_type": type(ex).__name__,
                "exc_message": traceback.format_exc().split("\n"),
            },
        )
        raise ex
