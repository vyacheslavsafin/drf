from rest_framework import serializers


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube.com' not in dict(value).get(self.field):
            raise serializers.ValidationError('Ссылка должна содержать youtube.com')
