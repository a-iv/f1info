import re
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserCreationForm.base_fields['username'].regex = re.compile(r'^[-\.\w]+$')
UserChangeForm.base_fields['username'].regex = re.compile(r'^[-\.\w]+$')
