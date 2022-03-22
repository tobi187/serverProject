import celery

cel_app = celery.Celery("test")

@cel_app.task()
def sample_task(x, y):
    return x +y