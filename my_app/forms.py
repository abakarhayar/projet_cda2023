# Importation du module forms de Django pour définir des formulaires
from django import forms
# Importation de la classe User du module auth.models de Django pour représenter les utilisateurs
from django.contrib.auth.models import User
# Importation des modèles définis dans le fichier models.py
from .models import Candidat, Entreprise, Emploi, Postuler, Competence, Experience, Formation
# Importation de la classe SetPasswordForm du module auth.forms de Django pour la gestion du mot de passe
from django.contrib.auth.forms import SetPasswordForm
# Importation du validateur personnalisé pour le mot de passe
from .validators import validate_password
# Importation de la fonction gettext_lazy du module django.utils.translation pour les traductions
from django.utils.translation import gettext_lazy as _
# Importation de la classe AuthenticationForm du module auth.forms de Django pour l'authentification
from django.contrib.auth.forms import AuthenticationForm
# Importation de la fonction authenticate du module auth de Django pour l'authentification de l'utilisateur
from django.contrib.auth import authenticate

# FORMULAIRE DES UTILISATEURS
# Définition de la classe UserForm qui hérite de forms.ModelForm
class UserForm(forms.ModelForm):
    # Définition d'un champ "username" avec un libellé personnalisé et un widget TextInput pour saisir le nom d'utilisateur
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': 'form-control'}))
    # Définition d'un champ "email" avec un libellé personnalisé et un widget EmailInput pour saisir l'email de l'utilisateur
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # Définition d'un champ "password" avec un libellé personnalisé et un widget PasswordInput pour saisir le mot de passe
    # Le champ est également associé au validateur de mot de passe personnalisé
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])
    # Définition d'un champ "confirm_password" avec un libellé personnalisé et un widget PasswordInput pour confirmer le mot de passe
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # Définition d'un champ "is_staff" avec un libellé personnalisé et un widget CheckboxInput pour indiquer si l'utilisateur est un administrateur
    is_staff = forms.BooleanField(label="Administrateur", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    # Définition d'un champ "is_active" avec un libellé personnalisé et un widget CheckboxInput pour activer/désactiver l'utilisateur
    is_active = forms.BooleanField(label="Activer l'utilisateur", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    # Classe Meta pour définir les informations du modèle lié au formulaire
    class Meta:
        # Le modèle lié est User, défini dans le modèle auth.models de Django
        model = User
        # Liste des champs à inclure dans le formulaire
        fields = ['username', 'email', 'password', 'confirm_password', 'is_staff', 'is_active']
        # Définition des widgets pour certains champs, en modifiant les attributs de l'élément HTML
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'confirm_password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    # Méthode clean pour valider les données du formulaire
    def clean(self):
        # Appel de la méthode clean() de la classe parent pour obtenir les données nettoyées
        cleaned_data = super().clean()
        # Récupération des champs password et confirm_password
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Validation : vérification si les mots de passe saisis correspondent
        if password and confirm_password and password != confirm_password:
            # Si les mots de passe ne correspondent pas, une erreur de validation est levée
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        # Retour des données nettoyées
        return cleaned_data

############# FORMULAIRE DE CANDIDAT ##################
# Formulaire pour le modèle Candidat
class CandidatForm(forms.ModelForm):
    # Champ pour le numéro de téléphone avec une longueur maximale de 10 caractères
    telephone = forms.CharField(label="Téléphone", max_length=10)

    class Meta:
        model = Candidat
        fields = ['nom', 'prenom', 'email', 'telephone', 'ville', 'cv']

    # Validation personnalisée pour le champ 'telephone'
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not str(telephone).isdigit() or len(str(telephone)) != 10:
            raise forms.ValidationError('Le numéro de téléphone doit contenir exactement 10 chiffres et pas des lettres.')

        # Vérification si le numéro de téléphone existe déjà dans la base de données
        # Uniquement si le candidat modifie son numéro de téléphone
        if self.instance.pk:  # Vérifier s'il s'agit d'une instance existante (mise à jour)
            candidat = Candidat.objects.get(pk=self.instance.pk)
            if candidat.telephone != telephone and Candidat.objects.filter(telephone=telephone).exists():
                raise forms.ValidationError('Ce numéro de téléphone est déjà enregistré. Utiliser un autre numéro.')

        return telephone

    # Champ pour le fichier du CV
    cv = forms.FileField(label='CV')


# Formulaire d'inscription pour le modèle User (candidat)
class InscriptionCandidatForm(forms.ModelForm):
    # Champ pour le mot de passe avec validation personnalisée
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])
    # Champ pour confirmer le mot de passe
    confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)
    # Champ pour l'adresse e-mail
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ['email', 'password']

    # Validation personnalisée pour le champ 'email'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet email est déjà utilisé. Veuillez choisir un autre.')
        return email

    # Validation personnalisée pour le champ 'confirm_password'
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return confirm_password

    # Sauvegarder l'utilisateur enregistré dans la base de données
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

# Formulaire pour ajouter un candidat
class AjouterCandidatForm(forms.ModelForm):
    # Champ pour le mot de passe avec validation personnalisée
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])
    # Champ pour confirmer le mot de passe
    confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)
    # Champ pour l'adresse e-mail
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ['email', 'password']

    # Validation personnalisée pour le champ 'email'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet email est déjà utilisé. Veuillez choisir un autre.')
        return email

    # Validation personnalisée pour le champ 'confirm_password'
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return confirm_password

    # Sauvegarder l'utilisateur enregistré dans la base de données
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

# Formulaire pour modifier un candidat
class ModificationCandidatForm(forms.ModelForm):
    # Champ pour le mot de passe avec validation personnalisée
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])
    # Champ pour confirmer le mot de passe
    confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)
    # Champ pour l'adresse e-mail
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ['email', 'password']

    # Validation personnalisée pour le champ 'email'
    def clean_email(self):
        email = self.cleaned_data.get('email')
        candidat = self.instance
        if User.objects.filter(email=email).exclude(pk=candidat.pk).exists():
            raise forms.ValidationError('Cet email est déjà utilisé. Veuillez choisir un autre.')
        return email

    # Validation personnalisée pour le champ 'confirm_password'
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return confirm_password

    # Sauvegarder les modifications de l'utilisateur dans la base de données
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

# Formulaire pour ajouter une postulation (candidature)
class AjouterPostulationForm(forms.ModelForm):
    # Champs pour sélectionner un candidat, une entreprise et un emploi
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label='Choisir un candidat')
    entreprise = forms.ModelChoiceField(queryset=Entreprise.objects.all(), empty_label='Choisir une entreprise')
    emploi = forms.ModelChoiceField(queryset=Emploi.objects.all(), empty_label='Choisir un emploi')
    
    # Choix de statut de candidature avec des options prédéfinies
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Consultée', 'Consultée'),
        ('Acceptée', 'Acceptée'),
        ('Selectionnée', 'Selectionnée'),
        ('Refusée', 'Refusée'),
    ]
    statutCandidature = forms.ChoiceField(choices=STATUT_CHOICES, initial='En attente')

    class Meta:
        model = Postuler
        fields = ['emploi', 'candidat', 'lettreMotivation', 'statutCandidature']

# Formulaire pour modifier une postulation (candidature)
class ModificationPostulationForm(forms.ModelForm):
    # Champs pour sélectionner un candidat, une entreprise et un emploi
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label='Choisir un candidat')
    entreprise = forms.ModelChoiceField(queryset=Entreprise.objects.all(), empty_label='Choisir une entreprise')
    emploi = forms.ModelChoiceField(queryset=Emploi.objects.all(), empty_label='Choisir un emploi')
    
    # Choix de statut de candidature avec des options prédéfinies
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Consultée', 'Consultée'),
        ('Acceptée', 'Acceptée'),
        ('Selectionnée', 'Selectionnée'),
        ('Refusée', 'Refusée'),
    ]
    statutCandidature = forms.ChoiceField(choices=STATUT_CHOICES, initial='En attente')

    class Meta:
        model = Postuler
        fields = ['emploi', 'candidat', 'lettreMotivation', 'statutCandidature']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnaliser le libellé pour le champ "emploi"
        self.fields['emploi'].label_from_instance = self.get_emploi_label

        # Définir les valeurs initiales pour les champs "candidat" et "entreprise"
        instance = kwargs.get('instance')
        if instance:
            self.fields['candidat'].initial = instance.candidat
            self.fields['entreprise'].initial = instance.emploi.entreprise

    def get_emploi_label(self, emploi_instance):
        # Personnaliser la façon dont le nom de l'emploi est affiché dans les options du menu déroulant
        return emploi_instance.titre  # Remplacez 'nom' par le nom de l'attribut réel pour le nom de l'emploi

# Formulaire pour ajouter une expérience
class AjouterExperienceForm(forms.ModelForm):
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label="Choisir un candidat")

    class Meta:
        model = Experience
        fields = ['candidat', 'entreprise', 'poste', 'description', 'dateDebut', 'dateFin']
        labels = {
            'dateDebut': "Date de début",
            "dateFin": "Date de fin"
        }

    # Utiliser un widget pour afficher un sélecteur de date
    date_widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(AjouterExperienceForm, self).__init__(*args, **kwargs)
        # Appliquer le widget de sélecteur de date aux champs de date
        self.fields['dateDebut'].widget = self.date_widget
        self.fields['dateFin'].widget = self.date_widget

# Formulaire pour modifier une expérience
class ModifierExperienceForm(forms.ModelForm):
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label="Choisir un candidat")

    class Meta:
        model = Experience
        fields = ['candidat', 'entreprise', 'poste', 'description', 'dateDebut', 'dateFin']
        labels = {
            'dateDebut': "Date de début",
            "dateFin": "Date de fin"
        }

    # Utiliser un widget pour afficher un sélecteur de date
    date_widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(ModifierExperienceForm, self).__init__(*args, **kwargs)
        # Appliquer le widget de sélecteur de date aux champs de date
        self.fields['dateDebut'].widget = self.date_widget
        self.fields['dateFin'].widget = self.date_widget

# Formulaire pour ajouter une compétence
class AjouterCompetenceForm(forms.ModelForm):
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label="Choisir un candidat")

    # Choix de niveau de maîtrise avec des options prédéfinies
    NIVEAU_CHOICES = [
        ('Débutant', 'Débutant'),
        ('Intermédiaire', 'Intermédiaire'),
        ('Avancé', 'Avancé'),
    ]

    niveau = forms.ChoiceField(choices=NIVEAU_CHOICES)

    class Meta:
        model = Competence
        fields = ['candidat', 'nom', 'niveau']
        labels = {
            'nom': "Nom de la compétence",
            "niveau": "Niveau de maîtrise",
        }

# Formulaire pour modifier une compétence
class ModifierCompetenceForm(forms.ModelForm):
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label="Choisir un candidat")

    # Choix de niveau de maîtrise avec des options prédéfinies
    NIVEAU_CHOICES = [
        ('Débutant', 'Débutant'),
        ('Intermédiaire', 'Intermédiaire'),
        ('Avancé', 'Avancé'),
    ]

    niveau = forms.ChoiceField(choices=NIVEAU_CHOICES)

    class Meta:
        model = Competence
        fields = ['candidat', 'nom', 'niveau']
        labels = {
            'nom': "Nom de la compétence",
            "niveau": "Niveau de maîtrise",
        }

# Formulaire pour ajouter une formation
class AjouterFormationForm(forms.ModelForm):
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label="Choisir un candidat")

    class Meta:
        model = Formation
        fields = ['candidat', 'titre', 'nom_ecole', 'ville', 'dateDebut', 'dateFin']
        labels = {
            'titre': "Titre de la formation",
            'nom_ecole': "Nom de l'école",
            'ville': "Ville",
            'dateDebut': "Date de début",
            'dateFin': "Date de fin",
        }
    # Utiliser un widget pour afficher un sélecteur de date
    date_widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(AjouterFormationForm, self).__init__(*args, **kwargs)
        # Ajouter des attributs personnalisés aux champs du formulaire si nécessaire
        self.fields['titre'].widget.attrs.update({'placeholder': "Entrez le titre de la formation"})
        self.fields['nom_ecole'].widget.attrs.update({'placeholder': "Entrez le nom de l'école"})
        self.fields['ville'].widget.attrs.update({'placeholder': "Entrez la ville"})
        # Appliquer le widget de sélecteur de date aux champs de date
        self.fields['dateDebut'].widget = self.date_widget
        self.fields['dateFin'].widget = self.date_widget

# Formulaire pour modifier une formation
class ModifierFormationForm(forms.ModelForm):
    candidat = forms.ModelChoiceField(queryset=Candidat.objects.all(), empty_label="Choisir un candidat")

    class Meta:
        model = Formation
        fields = ['candidat', 'titre', 'nom_ecole', 'ville', 'dateDebut', 'dateFin']
        labels = {
            'titre': "Titre de la formation",
            'nom_ecole': "Nom de l'école",
            'ville': "Ville",
            'dateDebut': "Date de début",
            'dateFin': "Date de fin",
        }
    # Utiliser un widget pour afficher un sélecteur de date
    date_widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(ModifierFormationForm, self).__init__(*args, **kwargs)
        # Ajouter des attributs personnalisés aux champs du formulaire si nécessaire
        self.fields['titre'].widget.attrs.update({'placeholder': "Entrez le titre de la formation"})
        self.fields['nom_ecole'].widget.attrs.update({'placeholder': "Entrez le nom de l'école"})
        self.fields['ville'].widget.attrs.update({'placeholder': "Entrez la ville"})
        # Appliquer le widget de sélecteur de date aux champs de date
        self.fields['dateDebut'].widget = self.date_widget
        self.fields['dateFin'].widget = self.date_widget

# Formulaire pour ajouter une compétence d'un candidat
class CompetenceForm(forms.ModelForm):
    # Définir un champ ForeignKey pour sélectionner un candidat

    # Choix de niveau de maîtrise avec des options prédéfinies
    NIVEAU_CHOICES = [
        ('Débutant', 'Débutant'),
        ('Intermédiaire', 'Intermédiaire'),
        ('Avancé', 'Avancé'),
    ]

    niveau = forms.ChoiceField(choices=NIVEAU_CHOICES)

    class Meta:
        model = Competence
        fields = ['nom', 'niveau']
        labels = {
            'nom': "Nom de la compétence",
            "niveau": "Niveau de maîtrise",
        }

# Formulaire pour ajouter une expérience d'un candidat
class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ['entreprise', 'poste', 'description', 'dateDebut', 'dateFin']
        labels = {
            'dateDebut': "Date de début",
            "dateFin": "Date de fin"
        }

    # Utiliser un widget pour afficher un sélecteur de date
    date_widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        # Appliquer le widget de sélecteur de date aux champs de date
        self.fields['dateDebut'].widget = self.date_widget
        self.fields['dateFin'].widget = self.date_widget

# Formulaire pour ajouter une formation d'un candidat
class FormationForm(forms.ModelForm):

    class Meta:
        model = Formation
        fields = ['titre', 'nom_ecole', 'ville', 'dateDebut', 'dateFin']
        labels = {
            'titre': "Titre de la formation",
            'nom_ecole': "Nom de l'école",
            'ville': "Ville",
            'dateDebut': "Date de début",
            'dateFin': "Date de fin",
        }
    # Utiliser un widget pour afficher un sélecteur de date
    date_widget = forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super(FormationForm, self).__init__(*args, **kwargs)
        # Ajouter des attributs personnalisés aux champs du formulaire si nécessaire
        self.fields['titre'].widget.attrs.update({'placeholder': "Entrez le titre de la formation"})
        self.fields['nom_ecole'].widget.attrs.update({'placeholder': "Entrez le nom de l'école"})
        self.fields['ville'].widget.attrs.update({'placeholder': "Entrez la ville"})
        # Appliquer le widget de sélecteur de date aux champs de date
        self.fields['dateDebut'].widget = self.date_widget
        self.fields['dateFin'].widget = self.date_widget

        
########### FORMULAIRE ENTREPRISE ############

# Formulaire pour l'enregistrement d'un nouvel utilisateur entreprise
class InscriptionEntrepriseForm(forms.ModelForm):
    # Définition des champs du formulaire
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email")

    # Définition du modèle et des champs du formulaire
    class Meta:
        model = User
        fields = ['email', 'password']

    # Validation personnalisée pour l'unicité de l'email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet email est déjà utilisé. Veuillez choisir un autre.')
        return email

    # Validation personnalisée pour la confirmation du mot de passe
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return confirm_password

    # Validation personnalisée pour la complexité du mot de passe
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise forms.ValidationError('Le mot de passe doit contenir au moins un chiffre et une lettre.')
        return password

    # Méthode de sauvegarde pour créer un nouvel utilisateur
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

# Formulaire pour la modification des informations de l'entreprise
class EntrepriseForm(forms.ModelForm):
    siren = forms.CharField(label="SIREN", max_length=19)
    telephone = forms.CharField(label="Téléphone", max_length=10)

    # Définition du modèle et des champs du formulaire
    class Meta:
        model = Entreprise
        fields = ['nom', 'siren', 'telephone', 'description', 'ville']

    # Validation personnalisée pour l'unicité et le format du SIREN
    def clean_siren(self):
        siren = self.cleaned_data.get('siren')
        if not str(siren).isdigit() or len(str(siren)) != 9:
            raise forms.ValidationError('Le numéro SIREN doit contenir exactement 9 chiffres et pas des lettres')

        # Vérification si le SIREN existe déjà dans la base de données et s'il a été modifié
        entreprise = self.instance
        if Entreprise.objects.filter(siren=siren).exclude(pk=entreprise.pk).exists():
            raise forms.ValidationError('Ce numéro SIREN est déjà enregistré. Utiliser un autre numéro.')

        return siren

    # Validation personnalisée pour l'unicité et le format du numéro de téléphone
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not str(telephone).isdigit() or len(str(telephone)) != 10:
            raise forms.ValidationError('Le numéro de téléphone doit contenir exactement 10 chiffres et pas des lettres.')

        # Vérification si le numéro de téléphone existe déjà dans la base de données et s'il a été modifié
        entreprise = self.instance
        if Entreprise.objects.filter(telephone=telephone).exclude(pk=entreprise.pk).exists():
            raise forms.ValidationError('Ce numéro de téléphone est déjà enregistré. Utiliser un autre numéro.')

        return telephone

# Formulaire pour l'ajout d'une nouvelle entreprise (utilise le formulaire InscriptionEntrepriseForm)
class AjouterEntrepriseForm(forms.ModelForm):
    # Définition des champs du formulaire (email et mot de passe) similaires à InscriptionEntrepriseForm
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email")

    # Définition du modèle et des champs du formulaire
    class Meta:
        model = User
        fields = ['email', 'password']

    # Validation personnalisée pour l'unicité de l'email (identique à InscriptionEntrepriseForm)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Cet email est déjà utilisé. Veuillez choisir un autre.')
        return email

    # Validation personnalisée pour la confirmation du mot de passe (identique à InscriptionEntrepriseForm)
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return confirm_password

    # Validation personnalisée pour la complexité du mot de passe (identique à InscriptionEntrepriseForm)
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise forms.ValidationError('Le mot de passe doit contenir au moins un chiffre et une lettre.')
        return password

    # Méthode de sauvegarde pour créer un nouvel utilisateur (identique à InscriptionEntrepriseForm)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user

# Formulaire pour la modification d'une entreprise (identique à AjouterEntrepriseForm)
class ModificationEntrepriseForm(forms.ModelForm):
    # Définition des champs du formulaire (email et mot de passe) similaires à InscriptionEntrepriseForm
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)
    email = forms.EmailField(label="Email")

    # Définition du modèle et des champs du formulaire
    class Meta:
        model = User
        fields = ['email', 'password']

    # Validation personnalisée pour l'unicité de l'email (identique à InscriptionEntrepriseForm)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        candidat = self.instance
        if User.objects.filter(email=email).exclude(pk=candidat.pk).exists():
            raise forms.ValidationError('Cet email est déjà utilisé. Veuillez choisir un autre.')
        return email

    # Validation personnalisée pour la confirmation du mot de passe (identique à InscriptionEntrepriseForm)
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return confirm_password

    # Validation personnalisée pour la complexité du mot de passe (identique à InscriptionEntrepriseForm)
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise forms.ValidationError('Le mot de passe doit contenir au moins un chiffre et une lettre.')
        return password

    # Sauvegarder les modifications de l'utilisateur dans la base de données
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

# Formulaire pour la modification d'une entreprise (identique à AjouterEntrepriseForm)

# Formulaire pour l'ajout d'un nouvel emploi
class AjouterEmploiForm(forms.ModelForm):
    entreprise = forms.ModelChoiceField(queryset=Entreprise.objects.all(), empty_label='Choisir une entreprise')
    CHOIX_CONTRAT = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Alternance', 'Alternance'),
        ('Stage', 'Stage'),
    ]

    CHOIX_DOMAINE = [
        ('Informatique', 'Informatique'),
        ('Marketing', 'Marketing'),
        ('Finance', 'Finance'),
        ('Ressources humaines', 'Ressources humaines'),
        ('Santé', 'Santé'),
        ('Bâtiment', 'Bâtiment'),
        ('Restauration', 'Restauration'),
        ('Immobilier', 'Immobilier'),
        ('Agriculture', 'Agriculture')
    ]

    type_contrat = forms.ChoiceField(choices=CHOIX_CONTRAT)
    domaine = forms.ChoiceField(choices=CHOIX_DOMAINE)

    class Meta:
        model = Emploi
        fields = ['titre', 'description', 'exigence', 'ville', 'salaire', 'type_contrat', 'domaine', 'entreprise']

    # Initialisation personnalisée pour définir la valeur initiale et masquer le champ entreprise (si nécessaire)
    def __init__(self, *args, **kwargs):
        entreprise_instance = kwargs.pop('entreprise_instance', None)
        super().__init__(*args, **kwargs)
        if entreprise_instance:
            self.fields['entreprise'].widget = forms.HiddenInput() 
            self.fields['entreprise'].initial = entreprise_instance.nom

# Formulaire pour la modification d'un emploi (hérite de AjouterEmploiForm)
class ModificationEmploiForm(AjouterEmploiForm):
    class Meta:
        model = Emploi
        fields = ['titre', 'description', 'exigence', 'ville', 'salaire', 'type_contrat', 'domaine']

# Formulaire pour la publication d'une offre d'emploi (similaire à AjouterEmploiForm mais sans le champ entreprise)
class EmploiForm(forms.ModelForm):
    CHOIX_CONTRAT = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('Alternance', 'Alternance'),
        ('Stage', 'Stage'),
    ]

    CHOIX_DOMAINE = [
        ('Informatique', 'Informatique'),
        ('Marketing', 'Marketing'),
        ('Finance', 'Finance'),
        ('Ressources humaines', 'Ressources humaines'),
        ('Santé', 'Santé'),
        ('Bâtiment', 'Bâtiment'),
        ('Restauration', 'Restauration'),
        ('Immobilier', 'Immobilier'),
        ('Agriculture', 'Agriculture')
    ]

    type_contrat = forms.ChoiceField(choices=CHOIX_CONTRAT)
    domaine = forms.ChoiceField(choices=CHOIX_DOMAINE)

    class Meta:
        model = Emploi
        fields = ['titre', 'description', 'exigence', 'ville', 'salaire', 'type_contrat', 'domaine']

# Formulaire pour postuler à un emploi
class CandidatureForm(forms.ModelForm):
    
    cv = forms.FileField(required=False)  # Champ pour télécharger le CV (optionnel)
    
    class Meta:
        model = Postuler
        fields = ['lettreMotivation', 'cv']  # Champs du modèle Postuler à afficher dans le formulaire

# Formulaire pour le choix de réponse de candidature par l'entreprise
class PostulerForm(forms.ModelForm):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Consultée', 'Consultée'),
        ('Acceptée', 'Acceptée'),
        ('Selectionnée', 'Selectionnée'),
        ('Refusée', 'Refusée'),
    ]

    statutCandidature = forms.ChoiceField(choices=STATUT_CHOICES, initial='En attente')  # Champ de sélection pour le statut de la candidature

    class Meta:
        model = Postuler
        fields = ('statutCandidature',)  # Champ du modèle Postuler à afficher dans le formulaire

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['statutCandidature'].empty_label = 'Choisir un statut'  # Label vide pour le champ de sélection

    def save(self, commit=True):
        postulation = super().save(commit=False)
        postulation.statutCandidature = self.cleaned_data['statutCandidature']  # Sauvegarde du statut de candidature

        if commit:
            postulation.save()
        return postulation

# Formulaire personnalisé pour le changement de mot de passe
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput, validators=[validate_password])  # Champ pour le nouveau mot de passe
    new_password2 = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))  # Champ pour la confirmation du nouveau mot de passe

    def clean(self):
       cleaned_data = super().clean()
       new_password1 = cleaned_data.get('new_password1')
       new_password2 = cleaned_data.get('new_password2')

       if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")  # Validation pour s'assurer que les mots de passe correspondent

       return cleaned_data

# Formulaire personnalisé pour la gestion d'erreurs en cas d'identifiants incorrects
class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("Compte inactif. Veuillez contacter l'administrateur."),
                code='inactive',
            )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("Email ou mot de passe incorrect. Veuillez réessayer."),
                    code='invalid_login',
                )  # Validation pour vérifier si les identifiants sont valides
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

# Formulaire pour envoyer un message
class MessageForm(forms.Form):
    contenu = forms.CharField(widget=forms.Textarea)  # Champ pour le contenu du message (zone de texte)
