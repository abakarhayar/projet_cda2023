from django.core.exceptions import ValidationError

def validate_password(password):
    # Définissez ici vos critères de complexité pour le mot de passe
    # Par exemple, vérifiez la longueur, la présence de majuscules, de minuscules, de chiffres et de caractères spéciaux
    if len(password) < 12:
        raise ValidationError("Le mot de passe doit contenir au moins 12 caractères.")
    if not any(char.isupper() for char in password):
        raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")
    if not any(char.islower() for char in password):
        raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
    if not any(char in '!@#$%^&*()' for char in password):
        raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial parmi !@#$%^&*().")
