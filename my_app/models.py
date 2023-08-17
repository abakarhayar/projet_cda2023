from django.db import models
from django.contrib.auth.models import User

# Modèle pour représenter un candidat
class Candidat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)  # Nom du candidat
    prenom = models.CharField(max_length=50)  # Prénom du candidat
    telephone = models.CharField(max_length=10, blank=True, null=True, unique=True)  # Numéro de téléphone du candidat (facultatif, unique)
    cv = models.FileField(upload_to='cv_files/', blank=True, null=True)  # Fichier CV du candidat (facultatif)
    ville = models.CharField(max_length=50, blank=True, null=True)  # Ville du candidat (facultatif)
    email = models.CharField(max_length=50, default='')  # Adresse e-mail du candidat (par défaut vide)

    def __str__(self):
        return self.nom + ' ' + self.prenom

# Modèle pour représenter une entreprise
class Entreprise(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)  # Nom de l'entreprise
    email = models.EmailField(max_length=100, default='')  # Adresse e-mail de l'entreprise (par défaut vide, longueur augmentée)
    telephone = models.CharField(max_length=10, blank=True, null=True, unique=True)  # Numéro de téléphone de l'entreprise (facultatif, unique)
    siren = models.CharField(max_length=9, blank=True, null=True, unique=True)  # Numéro SIREN de l'entreprise (facultatif, unique, longueur de 9 caractères)
    ville = models.CharField(max_length=50, blank=True, null=True)  # Ville de l'entreprise (facultatif)
    description = models.TextField(blank=True, null=True)  # Description de l'entreprise (facultatif)

    def __str__(self):
        return self.nom

# Modèle pour représenter les compétences des candidats
class Competence(models.Model):
    nom = models.CharField(max_length=50)  # Nom de la compétence
    niveau = models.CharField(max_length=50)  # Niveau de maîtrise de la compétence
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='competences')  # Clé étrangère liant la compétence au candidat

# Modèle pour représenter les formations des candidats
class Formation(models.Model):
    titre = models.CharField(max_length=50)  # Titre de la formation
    nom_ecole = models.CharField(max_length=50)  # Nom de l'école ou de l'institution
    ville = models.CharField(max_length=50)  # Ville de la formation
    dateDebut = models.DateField()  # Date de début de la formation
    dateFin = models.DateField()  # Date de fin de la formation
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='formations')  # Clé étrangère liant la formation au candidat

# Modèle pour représenter les expériences professionnelles des candidats
class Experience(models.Model):
    entreprise = models.CharField(max_length=50)  # Nom de l'entreprise
    poste = models.CharField(max_length=50)  # Poste occupé
    description = models.TextField(blank=True, null=True)  # Description de l'expérience (facultatif)
    dateDebut = models.DateField()  # Date de début de l'expérience
    dateFin = models.DateField()  # Date de fin de l'expérience
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='experiences')  # Clé étrangère liant l'expérience au candidat

# Modèle pour représenter les offres d'emploi
class Emploi(models.Model):
    titre = models.CharField(max_length=50)  # Titre de l'offre d'emploi
    description = models.TextField(blank=True, null=True)  # Description de l'offre d'emploi (facultatif)
    exigence = models.TextField(blank=True, null=True)  # Exigences de l'offre d'emploi (facultatif)
    ville = models.CharField(max_length=50)  # Ville de l'offre d'emploi
    salaire = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)  # Salaire de l'offre d'emploi (facultatif)
    type_contrat = models.CharField(max_length=50)  # Type de contrat de travail (CDI, CDD, etc.)
    domaine = models.CharField(max_length=50)  # Domaine de l'offre d'emploi
    datePublication = models.DateTimeField(auto_now_add=True)  # Date de publication de l'offre d'emploi
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='emplois')  # Clé étrangère liant l'offre d'emploi à l'entreprise

    def __str__(self):
        return self.titre

# Modèle pour représenter les candidatures aux offres d'emploi
class Postuler(models.Model):
    emploi = models.ForeignKey(Emploi, on_delete=models.CASCADE)  # Clé étrangère liant la candidature à l'offre d'emploi
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)  # Clé étrangère liant la candidature au candidat
    dateCandidature = models.DateField(auto_now_add=True)  # Date de la candidature
    lettreMotivation = models.TextField()  # Lettre de motivation du candidat pour la candidature
    statutCandidature = models.CharField(max_length=20, default='En attente')  # Statut de la candidature (En attente, Acceptée, Refusée, etc.)

# Modèle pour représenter les messages échangés entre l'entreprise et le candidat
class Message(models.Model):
    contenu = models.TextField()  # Contenu du message
    date_message = models.DateTimeField(auto_now_add=True)  # Date et heure du message
    expediteur = models.ForeignKey(User, on_delete=models.CASCADE)  # Clé étrangère liant l'expéditeur (utilisateur) au message

# Modèle pour représenter une conversation entre une entreprise et un candidat
class Conversation(models.Model):
    entreprise = models.ForeignKey(User, related_name='conversations_entreprise', on_delete=models.CASCADE)  # Clé étrangère liant l'entreprise à la conversation
    candidat = models.ForeignKey(User, related_name='conversations_candidat', on_delete=models.CASCADE)  # Clé étrangère liant le candidat à la conversation
    messages = models.ManyToManyField(Message)  # Relation ManyToMany pour les messages de la conversation

    class Meta:
        unique_together = ['entreprise', 'candidat']  # Contrainte pour garantir l'unicité de la conversation entre l'entreprise et le candidat
