from bucket import bucket
from celery import shared_task


# TODO: can be async
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result


@shared_task
def delete_bucket_object_task(key):
    result = bucket.delete_object(key)
    return True


@shared_task
def download_bucket_object_task(key):
    result = bucket.download_object(key)
    return result
