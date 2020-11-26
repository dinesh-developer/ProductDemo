from rest_framework import exceptions


def validate_headers(request):
    platform = request.META.get('HTTP_PLATFORM', None)
    app_version = request.META.get('HTTP_APP_VERSION', None)
    device_id = request.META.get('HTTP_DEVICE_ID', None)
    if not device_id:
        raise exceptions.ValidationError(detail="The device_id field is required.")
    if not platform:
        raise exceptions.ValidationError(detail="The platform field is required.")
    if not app_version:
        raise exceptions.ValidationError(detail="The app_version field is required.")
    return platform, app_version, device_id