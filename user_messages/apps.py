from django.apps import AppConfig


class UserMessagesConfig(AppConfig):  # 改為 UserMessagesConfig
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_messages"  # 這裡改成新的資料夾名稱