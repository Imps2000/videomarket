from django.apps import AppConfig

class SubmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'submissions'
    
    def ready(self):
        """앱 로드 시 시그널 등록"""
        import submissions.signals  # noqa