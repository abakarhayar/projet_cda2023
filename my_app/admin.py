from django.contrib import admin
from .models import Candidat, Entreprise, Competence, Formation, Experience, Emploi, Postuler, Message, Conversation

# Enregistrement des modèles dans l'interface d'administration

@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'telephone']
    search_fields = ['nom', 'prenom', 'email', 'telephone']

@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'telephone', 'siren']
    search_fields = ['nom', 'email', 'telephone', 'siren']

@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'niveau', 'candidat']
    search_fields = ['nom', 'niveau', 'candidat__nom', 'candidat__prenom']

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'nom_ecole', 'ville', 'dateDebut', 'dateFin', 'candidat']
    search_fields = ['titre', 'nom_ecole', 'ville', 'candidat__nom', 'candidat__prenom']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['entreprise', 'poste', 'dateDebut', 'dateFin', 'candidat']
    search_fields = ['entreprise', 'poste', 'candidat__nom', 'candidat__prenom']

@admin.register(Emploi)
class EmploiAdmin(admin.ModelAdmin):
    list_display = ['titre', 'entreprise', 'ville', 'type_contrat', 'domaine', 'datePublication']
    search_fields = ['titre', 'entreprise__nom', 'ville', 'type_contrat', 'domaine']

@admin.register(Postuler)
class PostulerAdmin(admin.ModelAdmin):
    list_display = ['emploi', 'candidat', 'dateCandidature', 'statutCandidature']
    search_fields = ['emploi__titre', 'candidat__nom', 'candidat__prenom', 'statutCandidature']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['contenu', 'date_message', 'expediteur']
    search_fields = ['contenu', 'expediteur__username']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['entreprise', 'candidat']
    search_fields = ['entreprise__username', 'candidat__username']
