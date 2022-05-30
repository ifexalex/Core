from django.db import models
from django.contrib.auth import get_user_model

# Getting the user model from the settings.py file.
User = get_user_model()


class PhoneNumber(models.Model):
    number = models.CharField(
        max_length=40, help_text="This designates the Phone number"
    )
    account_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="This designates the account_id associated with the Phone number",
    )

    def __str__(self):
        return f"{self.number} associated with {self.account_id.username}"
