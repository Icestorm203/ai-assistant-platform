from app.tasks.celery_app import celery_app


def test_celery_loaded():

    assert celery_app is not None