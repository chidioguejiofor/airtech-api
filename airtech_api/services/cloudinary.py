import cloudinary.uploader
from celery_config import celery_app


from airtech_api.users.models import User


@celery_app.task(name='upload-profile-picture')
def upload_profile_picture(user_id, image_public_id, filename):
    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = project_root.rsplit('/', 1)[0]
    full_file_path = project_root + '/' +filename

    try:
        upload_response = cloudinary.uploader.upload(filename)
    except Exception:
        upload_response = None

    if os.path.isfile(full_file_path):
        os.remove(full_file_path)

    if image_public_id and upload_response:
        cloudinary.uploader.destroy(image_public_id)

    if upload_response:
        User.objects.filter(pk=user_id).update(image_public_id=upload_response['public_id'], image_url=upload_response['secure_url'])
        return 'Success'

    return 'Failure'
