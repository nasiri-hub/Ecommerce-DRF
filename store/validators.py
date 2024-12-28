from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_mb = 5

    if file.size > max_size_mb * (1024 ** 2):
        raise ValidationError(f'Files cannot be larger than {max_size_mb}MB!')
