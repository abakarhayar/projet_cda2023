# Importation de fonctions utiles pour le rendu de templates et la redirection
from django.shortcuts import render, redirect, get_object_or_404
# Importation de la classe de vue permettant de changer le mot de passe
from django.contrib.auth.views import PasswordChangeView
# Importation de fonctions pour l'authentification de l'utilisateur, la connexion et la déconnexion
from django.contrib.auth import authenticate, login, logout
# Importation de classes pour afficher des messages à l'utilisateur
from django.contrib import messages
# Import des différents formulaires utilisés dans les vues
from .forms import (InscriptionCandidatForm, CandidatForm, InscriptionEntrepriseForm, EntrepriseForm,
                    CustomSetPasswordForm, EmploiForm, CandidatureForm, PostulerForm, CompetenceForm,
                    ExperienceForm, FormationForm, MessageForm, ModificationCandidatForm, UserForm,
                    ModificationEntrepriseForm, AjouterCandidatForm, AjouterEntrepriseForm,
                    AjouterEmploiForm, ModificationEmploiForm, AjouterPostulationForm,
                    ModificationPostulationForm, AjouterExperienceForm, AjouterCompetenceForm,
                    ModifierExperienceForm, ModifierCompetenceForm, AjouterFormationForm,
                    ModifierFormationForm, CustomAuthenticationForm)

# Import des modèles définis dans le projet
from .models import Entreprise, Emploi, Candidat, Conversation, Message, User, Competence, Formation, Experience, Postuler

# Import de la classe de formulaire d'authentification par défaut de Django
from django.contrib.auth.forms import AuthenticationForm

# Import des décorateurs pour restreindre l'accès aux vues aux utilisateurs authentifiés ou ayant des permissions spécifiques
from django.contrib.auth.decorators import login_required, user_passes_test

# Import des fonctions pour l'envoi d'e-mails
from django.core.mail import send_mail

# Import des paramètres de configuration du projet
from django.conf import settings

# Import d'éléments utiles pour le rendu d'e-mails en HTML et suppression des balises HTML
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Import de la fonction pour hasher les mots de passe
from django.contrib.auth.hashers import make_password
# Importer la classe HttpResponse du module http de Django.
# Cette classe permet de créer des réponses HTTP à renvoyer au client.
from django.http import HttpResponse

# Vue pour la page d'accueil qui affiche les offres d'emploi récentes
def home(request):
    # Récupération de tous les objets "Emploi" de la base de données et stockage dans une variable "emplois"
    emplois = Emploi.objects.all()
    # Renvoi d'une réponse HTTP à la requête avec le template "home.html" et un dictionnaire de contexte
    # La clé "emplois" est associée à la variable "emplois" créée précédemment
    return render(request, 'home.html', {'emplois': emplois})

# Vue pour la page de connexion admin
def connexion_admin(request):
    # Vérifie si la méthode de la requête est POST (utilisée lors de la soumission du formulaire)
    if request.method == 'POST':
        # Crée un formulaire d'authentification (AuthenticationForm) avec les données POST de la requête
        form = AuthenticationForm(request=request, data=request.POST)
        
        # Vérifie si le formulaire est valide (c'est-à-dire si les champs sont correctement remplis)
        if form.is_valid():
            # Récupère le nom d'utilisateur (username) et le mot de passe (password) du formulaire validé
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authentifie l'utilisateur en vérifiant les informations d'identification (nom d'utilisateur et mot de passe)
            # La fonction authenticate retourne l'utilisateur correspondant s'il existe, sinon None
            user = authenticate(request, username=username, password=password)
            
            # Vérifie si l'utilisateur existe et est un administrateur (user.is_staff est True pour les administrateurs)
            if user is not None and user.is_staff:
                # Connecte l'utilisateur en créant une session pour lui (utilisant le système d'authentification de Django)
                login(request, user)
                
                # Redirige l'utilisateur vers la vue 'dashboard' (interface d'administration)
                return redirect('dashboard')
                
    else:
        # Si la méthode de la requête n'est pas POST (première visite de la page), crée un nouveau formulaire vide
        form = AuthenticationForm()
    
    # Renvoie le template 'admin/connexion_admin.html' avec le formulaire en contexte
    return render(request, 'admin/connexion_admin.html', {'form': form})

# Vue pour la déconnexion de tous les utilisateurs
@login_required
def deconnexion(request):
    logout(request)
    return redirect('home')    

# Vue pour la page d'accueil du tableau de bord d'administration (dashboard)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def dashboard(request):
    # Vérifie si l'utilisateur n'est pas un superutilisateur (administrateur), renvoie une réponse "Accès refusé"
    if not request.user.is_superuser:
        return HttpResponse("Accès refusé")

    # Récupération de toutes les instances des modèles depuis la base de données
    # Ces instances seront utilisées pour afficher différentes statistiques dans le tableau de bord
    candidats = Candidat.objects.all()
    entreprises = Entreprise.objects.all()
    emplois = Emploi.objects.all()
    users = User.objects.all()
    competences = Competence.objects.all()
    formations = Formation.objects.all()
    experiences = Experience.objects.all()
    conversations = Conversation.objects.all()
    messages = Message.objects.all()
    postulations = Postuler.objects.all()

    # Création d'un dictionnaire de contexte contenant toutes les instances des modèles
    context = {
        'candidats': candidats,
        'entreprises': entreprises,
        'emplois': emplois,
        'users': users,
        'competences': competences,
        'formations': formations,
        'experiences': experiences,
        'conversations': conversations,
        'messages': messages,
        'postulations': postulations
    }

    # Renvoi d'une réponse HTTP à la requête avec le template "admin/dashboard.html" et le dictionnaire de contexte
    return render(request, 'admin/dashboard.html', context)

# Vue pour supprimer un utilisateur (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def supprimer_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('dashboard')

    return render(request, 'admin/users/supprimer_user.html', {'user': user}) 

# Vue pour ajouter un utilisateur (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def ajouter_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserForm()

    return render(request, 'admin/users/ajouter_user.html', {'form': form})

# Vue pour modifier un utilisateur (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def modifier_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # Récupérer le mot de passe saisi dans le formulaire
            password = form.cleaned_data.get('password')
            if password:
                # Hacher le mot de passe
                hashed_password = make_password(password)
                # Mettre à jour le mot de passe dans le formulaire
                form.instance.password = hashed_password

            form.save()
            return redirect('dashboard')
    else:
        form = UserForm(instance=user)

    return render(request, 'admin/users/modifier_user.html', {'form': form})

# Vue pour ajouter un candidat (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def ajouter_candidat(request):
    if request.method == 'POST':
        user_form = AjouterCandidatForm(request.POST)
        candidat_form = CandidatForm(request.POST, request.FILES)
        if user_form.is_valid() and candidat_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.username = user_form.cleaned_data['email']
            user.save()
            candidat = candidat_form.save(commit=False)
            candidat.email = user_form.cleaned_data['email']
            candidat.user = user
            candidat.save()
            return redirect('dashboard')
    else:
        user_form = AjouterCandidatForm()
        candidat_form = CandidatForm()
    return render(request, 'admin/candidats/ajouter_candidat.html', {'user_form': user_form, 'candidat_form': candidat_form})

# Vue pour modifier un candidat (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def modifier_candidat(request, candidat_id):
    # Récupération du candidat à partir de son ID. Si aucun candidat avec cet ID n'existe, une erreur 404 est renvoyée.
    candidat = get_object_or_404(Candidat, id=candidat_id)
    
    if request.method == 'POST':
        # Création des formulaires à partir des données envoyées par la requête, en utilisant l'instance du candidat actuel pour la modification
        user_form = ModificationCandidatForm(request.POST, instance=candidat.user)
        candidat_form = CandidatForm(request.POST, request.FILES, instance=candidat)
        
        # Vérification si les deux formulaires sont valides
        if user_form.is_valid() and candidat_form.is_valid():
            # Sauvegarde du formulaire utilisateur (User)
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.username = user_form.cleaned_data['email']
            user.save()
            
            # Sauvegarde du formulaire candidat (Candidat)
            candidat = candidat_form.save(commit=False)
            candidat.email = user_form.cleaned_data['email']
            candidat.user = user
            candidat.save()
            
            return redirect('dashboard')  # Redirige l'utilisateur vers le tableau de bord de l'administration après avoir modifié le candidat

    else:
        # Si la requête n'est pas de type POST, on crée des formulaires avec les données actuelles du candidat
        user_form = ModificationCandidatForm(instance=candidat.user)
        candidat_form = CandidatForm(instance=candidat)

    # Renvoi d'une réponse HTTP à la requête avec le template "admin/candidats/modifier_candidat.html" et les formulaires
    # ainsi que l'ID du candidat pour l'utiliser dans le template si nécessaire.
    return render(request, 'admin/candidats/modifier_candidat.html', {'user_form': user_form, 'candidat_form': candidat_form, 'candidat_id': candidat_id})

# Vue pour supprimer un candidat (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def supprimer_candidat(request, candidat_id):
    candidat = get_object_or_404(Candidat, id=candidat_id)
    if request.method == 'POST':
        candidat.delete()
        return redirect('dashboard')

    return render(request, 'admin/candidats/supprimer_candidat.html', {'candidat': candidat})

# ADMIN: GESTION ENTREPRISE
# Vue pour ajouter une entreprise (admin)
@user_passes_test(lambda u: u.is_superuser)
def ajouter_entreprise(request):
    if request.method == 'POST':
        user_form = AjouterEntrepriseForm(request.POST)
        entreprise_form = EntrepriseForm(request.POST)
        if user_form.is_valid() and entreprise_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.username = user_form.cleaned_data['email']  
            user.save()
            entreprise = entreprise_form.save(commit=False)
            entreprise.email = user_form.cleaned_data['email']  
            entreprise.user = user
            entreprise.save()
            return redirect('dashboard')
                    
    else:
        user_form = AjouterEntrepriseForm()
        entreprise_form = EntrepriseForm()
    return render(request, 'admin/entreprises/ajouter_entreprise.html', {'user_form': user_form, 'entreprise_form': entreprise_form})

# Vue pour modifier une entreprise (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder  
def modifier_entreprise(request, entreprise_id):
    entreprise = Entreprise.objects.get(pk=entreprise_id)

    if request.method == 'POST':
        user_form = ModificationEntrepriseForm(request.POST, instance=entreprise.user)
        entreprise_form = EntrepriseForm(request.POST, instance=entreprise)
        if user_form.is_valid() and entreprise_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.username = user_form.cleaned_data['email']
            user.save()
            entreprise = entreprise_form.save(commit=False)
            entreprise.email = user_form.cleaned_data['email']
            entreprise.user = user
            entreprise.save()
            return redirect('dashboard')
    else:
        user_form = ModificationEntrepriseForm(instance=entreprise.user)
        entreprise_form = EntrepriseForm(instance=entreprise)
    return render(request, 'admin/entreprises/modifier_entreprise.html',  {'user_form': user_form, 'entreprise_form': entreprise_form, 'entreprise_id': entreprise_id})

# Vue pour supprimer une entreprise (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def supprimer_entreprise(request, entreprise_id):
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)
    if request.method == 'POST':
        entreprise.delete()
        return redirect('dashboard')

    return render(request, 'admin/entreprises/supprimer_entreprise.html', {'entreprise': entreprise}) 

# ADMIN: GESTION EMPLOI
# Vue pour ajouter un emploi (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def ajouter_emploi(request):
    if request.method == 'POST':
        form = AjouterEmploiForm(request.POST)
        if form.is_valid():
            emploi = form.save()
            return redirect('dashboard') 
    else:
        entreprise_instance = None
        try:
            entreprise_instance = Entreprise.objects.get(user=request.user)
        except Entreprise.DoesNotExist:
            pass

        form = AjouterEmploiForm(entreprise_instance=entreprise_instance)

    return render(request, 'admin/emplois/ajouter_emploi.html', {'form': form})

# Vue pour modifier un emploi (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def modifier_emploi(request, emploi_id):
    emploi = get_object_or_404(Emploi, pk=emploi_id)

    if request.method == 'POST':
        form = ModificationEmploiForm(request.POST, instance=emploi)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = ModificationEmploiForm(instance=emploi)

    return render(request, 'admin/emplois/modifier_emploi.html', {'form': form}) 

# Vue pour supprimer un emploi (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def supprimer_emploi(request, emploi_id):
    emploi = get_object_or_404(Emploi, id=emploi_id)
    if request.method == 'POST':
        emploi.delete()
        return redirect('dashboard')
    return render(request, 'admin/emplois/supprimer_emploi.html', {'emploi': emploi}) 

# ADMIN: GESTION DE POSTULATION
# Vue pour ajouter une postulation (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def ajouter_postulation(request):
    if request.method == 'POST':
        form = AjouterPostulationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirigez où vous voulez après avoir ajouté la candidature
    else:
        form = AjouterPostulationForm()

    return render(request, 'admin/postulations/ajouter_postulation.html', {'form': form}) 

# Vue pour modifier une postulation (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def modifier_postulation(request, postulation_id):
    # Récupérer l'instance de la postulation à modifier
    postulation = get_object_or_404(Postuler, pk=postulation_id)

    if request.method == 'POST':
        # Créer une instance du formulaire avec les données soumises
        form = ModificationPostulationForm(request.POST, instance=postulation)
        if form.is_valid():
            form.save()  # Sauvegarder les modifications
            return redirect('dashboard')
    else:
        # Initialiser le formulaire avec les valeurs actuelles de la postulation
        form = ModificationPostulationForm(instance=postulation)

    return render(request, 'admin/postulations/modifier_postulation.html', {'form': form}) 

# Vue pour supprimer une postulation (admin)
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def supprimer_postulation(request, postulation_id):
    postulation = get_object_or_404(Postuler, id=postulation_id)
    if request.method == 'POST':
        postulation.delete()
        return redirect('dashboard')
    return render(request, 'admin/postulations/supprimer_postulation.html', {'postulation': postulation}) 


# ADMIN: GESTION EXPERIENCE    
# admin: ajouter expérience
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def ajouter_experience(request):
    if request.method == 'POST':
        form = AjouterExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = AjouterExperienceForm()

    return render(request, 'admin/experiences/ajouter_experience.html', {'form': form})

# admin: modifier expérience
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def modifier_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)

    if request.method == 'POST':
        form = ModifierExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = ModifierExperienceForm(instance=experience)

    return render(request, 'admin/experiences/modifier_experience.html', {'form': form})

# admin: supprimer expérience
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def supprimer_experience(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)
    if request.method == 'POST':
        experience.delete()
        return redirect('dashboard')
    return render(request, 'admin/experiences/supprimer_experience.html', {'experience': experience})

# ADMIN: GESTION COMPETENCE
# admin: ajouter compétence
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def ajouter_competence(request):
    if request.method == 'POST':
        form = AjouterCompetenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = AjouterCompetenceForm()

    return render(request, 'admin/competences/ajouter_competence.html', {'form': form})   

# admin: modifier compétence
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def modifier_competence(request, competence_id):
    competence = get_object_or_404(Competence, id=competence_id)
    if request.method == 'POST':
        form = ModifierCompetenceForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = ModifierCompetenceForm(instance=competence)

    return render(request, 'admin/competences/modifier_competence.html', {'form': form})    

# admin: supprimer compétence
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def supprimer_competence(request, competence_id):
    competence = get_object_or_404(Competence, id=competence_id)
    if request.method == 'POST':
        competence.delete()
        return redirect('dashboard')
    return render(request, 'admin/competences/supprimer_competence.html', {'competence': competence})     

# ADMIN: GESTION FORMATION    
# admin: ajouter formation
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def ajouter_formation(request):
    if request.method == 'POST':
        form = AjouterFormationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Rediriger vers une page de succès après avoir enregistré le formulaire avec succès
    else:
        form = AjouterFormationForm()

    return render(request, 'admin/formations/ajouter_formation.html', {'form': form})   

# admin: modifier formation
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder
def modifier_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)

    if request.method == 'POST':
        form = ModifierFormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  
    else:
        form = ModifierFormationForm(instance=formation)

    return render(request, 'admin/formations/modifier_formation.html', {'form': form})   
# admin: supprimer formation
@user_passes_test(lambda u: u.is_superuser)  # Vue protégée, seuls les administrateurs peuvent y accéder     
def supprimer_formation(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST':
        formation.delete()
        return redirect('dashboard')
    return render(request, 'admin/formations/supprimer_formation.html', {'formation': formation}) 



############# CANDIDAT #############################

# inscription de candidat
def inscription_candidat(request):
    if request.method == 'POST':
        # Récupère le formulaire de création de compte utilisateur (email, mot de passe, etc.).
        user_form = InscriptionCandidatForm(request.POST)
        # Récupère le formulaire d'informations du candidat (nom, prénom, photo, etc.).
        candidat_form = CandidatForm(request.POST, request.FILES)
        if user_form.is_valid() and candidat_form.is_valid():
            # Enregistre le compte utilisateur.
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.username = user_form.cleaned_data['email']
            user.save()

            # Enregistre les informations du candidat associées au compte utilisateur.
            candidat = candidat_form.save(commit=False)
            candidat.email = user_form.cleaned_data['email']
            candidat.user = user
            candidat.save()

            # Authentifie l'utilisateur et le connecte après l'inscription.
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profil_candidat')
    else:
        user_form = InscriptionCandidatForm()
        candidat_form = CandidatForm()
    return render(request, 'candidats/inscription_candidat.html', {'user_form': user_form, 'candidat_form': candidat_form})

# connexion candidat
def connexion_candidat(request):
    if request.method == 'POST':
        # Récupère le formulaire de connexion personnalisé (email, mot de passe).
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            # Authentifie l'utilisateur et le connecte.
            user = form.get_user()
            login(request, user)
            return redirect('profil_candidat')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'candidats/connexion_candidat.html', {'form': form})

# page accueil candidat
@login_required
def profil_candidat(request):
    # Cette vue affiche le profil du candidat actuellement connecté.
    # Récupère l'utilisateur connecté à partir de l'objet "request".
    user = request.user
    # Récupère le profil de candidat associé à l'utilisateur connecté.
    candidat = user.candidat 
    context = {
        'user': user,
        'candidat': candidat,
    }
    return render(request, 'candidats/profil_candidat.html', context)  

# modifier profil candidat
@login_required
def modifier_profile_candidat(request, candidat_id):
    # Cette vue permet au candidat de modifier son profil.
    user = request.user
    candidat = user.candidat
    candidat= get_object_or_404(Candidat, id=candidat_id)

    if request.method == 'POST':
        # Récupère le formulaire de modification des informations du candidat.
        form = CandidatForm(request.POST, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('profil_candidat')
    else:
        form = CandidatForm(instance=candidat)

    context = {
        'form': form
    }
    return render(request, 'candidats/modifier_profile_candidat.html', context)

# candidat : ajouter compétence   
@login_required 
def ajouterCompetence(request):
    # Cette vue permet au candidat d'ajouter une compétence à son profil.
    # Récupère l'utilisateur connecté à partir de l'objet "request".
    user = request.user
    # Récupère le profil de candidat associé à l'utilisateur connecté.
    candidat = user.candidat 
    if request.method == 'POST':
        # Récupère le formulaire d'ajout de compétence.
        form = CompetenceForm(request.POST)
        if form.is_valid():
            competence = form.save(commit=False)
            competence.candidat = candidat
            competence.save()
            return redirect('profil_candidat') 

    else:
        form = CompetenceForm()

    context = {
        'form' : form
    }
    return render(request, 'candidats/ajouterCompetence.html', context)    

# candidat: modifier compétence
@login_required
def modifierCompetence(request, competence_id):
    # Cette vue permet au candidat de modifier une compétence de son profil.
    user = request.user
    candidat = user.candidat
    try:
        competence = Competence.objects.get(id=competence_id, candidat=candidat)
    except Competence.DoesNotExist:
        return HttpResponse("La compétence n'existe pas ou vous n'êtes pas autorisé à la modifier.")

    if request.method == 'POST':
        # Récupère le formulaire de modification de compétence.
        form = CompetenceForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            return redirect('profil_candidat')  
    else:
        form = CompetenceForm(instance=competence)

    context = {
        'form': form
    }

    return render(request, 'candidats/modifierCompetence.html', context)    

# candidat: supprimer compétence
@login_required
def supprimerCompetence(request, competence_id):
    # Cette vue permet au candidat de supprimer une compétence de son profil.
    competence = get_object_or_404(Competence, id=competence_id)
    if request.method == 'POST':
        competence.delete()
        return redirect('profil_candidat')
    return render(request, 'candidats/supprimerCompetence.html', {'competence': competence})             

# candidat: ajouter expérience
@login_required
def ajouterExperience(request):
    # Cette vue permet au candidat d'ajouter une expérience à son profil.
    user = request.user
    candidat = user.candidat

    if request.method == 'POST':
        # Récupère le formulaire d'ajout d'expérience.
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.candidat = candidat
            experience.save()
            return redirect('profil_candidat') 
    else:
        form = ExperienceForm()

    context = {
        'form': form
    }
    return render(request, 'candidats/ajouterExperience.html', context)    

# candidat: modifier expérience
@login_required
def modifierExperience(request, experience_id):
    # Cette vue permet au candidat de modifier une expérience de son profil.
    user = request.user
    candidat = user.candidat
    experience = get_object_or_404(Experience, id=experience_id, candidat=candidat)

    if request.method == 'POST':
        # Récupère le formulaire de modification d'expérience.
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('profil_candidat')  
    else:
        form = ExperienceForm(instance=experience)

    context = {
        'form': form
    }
    return render(request, 'candidats/modifierExperience.html', context)    

# candidat: supprimer expérience
@login_required
def supprimerExperience(request, experience_id):
    # Cette vue permet au candidat de supprimer une expérience de son profil.
    experience = get_object_or_404(Experience, id=experience_id)
    if request.method == 'POST':
        experience.delete()
        return redirect('profil_candidat')
    return render(request, 'candidats/supprimerExperience.html', {'experience': experience}) 

# candidat: ajouter formation
@login_required
def ajouterFormation(request):
    # Cette vue permet au candidat d'ajouter une formation à son profil.
    user = request.user
    candidat = user.candidat

    if request.method == 'POST':
        # Récupère le formulaire d'ajout de formation.
        form = FormationForm(request.POST)
        if form.is_valid():
            formation = form.save(commit=False)
            formation.candidat = candidat
            formation.save()
            return redirect('profil_candidat') 
        form = FormationForm()

    context = {
        'form': form
    }
    return render(request, 'candidats/ajouterFormation.html', context)

# candidat: modifier formation
@login_required
def modifierFormation(request, formation_id):
    # Cette vue permet au candidat de modifier une formation de son profil.
    user = request.user
    candidat = user.candidat
    formation = get_object_or_404(Formation, id=formation_id, candidat=candidat)

    if request.method == 'POST':
        # Récupère le formulaire de modification de formation.
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('profil_candidat')  
    else:
        form = FormationForm(instance=formation)

    context = {
        'form': form
    }
    return render(request, 'candidats/modifierFormation.html', context)

# candidat: supprimer formation
@login_required
def supprimerFormation(request, formation_id):
    # Cette vue permet au candidat de supprimer une formation de son profil.
    formation = get_object_or_404(Formation, id=formation_id)
    if request.method == 'POST':
        formation.delete()
        return redirect('profil_candidat')
    return render(request, 'candidats/supprimerFormation.html', {'formation': formation})         

# candidat: postuler à un emploi
def postuler_emploi(request, emploi_id):
    # Cette vue permet au candidat de postuler à un emploi.
    emploi = get_object_or_404(Emploi, id=emploi_id)
    
    if not request.user.is_authenticated or not request.user.candidat:
        # Vérifie si l'utilisateur est connecté en tant que candidat avant de permettre la candidature.
        messages.error(request, "Vous devez être un candidat pour postuler à un emploi.")
        return redirect('connexion_candidat')
    
    if request.method == 'POST':
        # Récupère le formulaire de candidature.
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.emploi = emploi
            candidature.candidat = request.user.candidat
            candidature.save()
            
            # Envoi de l'e-mail de confirmation de candidature au candidat.
            subject = "Confirmation de candidature"
            message = render_to_string('candidatures/email_candidature.html', {'candidature': candidature})
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'hiriberiasso@gmail.com', [request.user.candidat.email], html_message=message)
            
            messages.success(request, "Votre candidature à l'emploi a été envoyée avec succès. Veuillez vérifier votre boîte de réception pour la confirmation.")
            return redirect('home')
    else:
        form = CandidatureForm()
    
    context = {
        'emploi': emploi,
        'form': form
    }
    return render(request, 'candidatures/postuler_emploi.html', context)

# candidat: liste des candidatures postulées
@login_required
def mes_candidatures(request, candidat_id):
    # Cette vue affiche la liste des candidatures postulées par un candidat.
    candidat = get_object_or_404(Candidat, id=candidat_id)
    candidatures = Postuler.objects.filter(candidat=candidat)
    context = {
        'candidat': candidat,
        'candidatures': candidatures
    }
    return render(request, 'candidats/mes_candidatures.html', context)

############## ENTREPRISE ####################

# vue inscription entreprise
def inscription_entreprise(request):
    if request.method == 'POST':
        # Récupère le formulaire de création de compte utilisateur (email, mot de passe, etc.).
        user_form = InscriptionEntrepriseForm(request.POST)
        # Récupère le formulaire d'informations de l'entreprise (nom, adresse, etc.).
        entreprise_form = EntrepriseForm(request.POST)
        if user_form.is_valid() and entreprise_form.is_valid():
            # Enregistre le compte utilisateur.
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.username = user_form.cleaned_data['email']
            user.save()

            # Enregistre les informations de l'entreprise associées au compte utilisateur.
            entreprise = entreprise_form.save(commit=False)
            entreprise.email = user_form.cleaned_data['email']
            entreprise.user = user
            entreprise.save()

            # Authentifie l'utilisateur et le connecte après l'inscription.
            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('profil_entreprise')
    else:
        user_form = InscriptionEntrepriseForm()
        entreprise_form = EntrepriseForm()
    return render(request, 'entreprises/inscription_entreprise.html', {'user_form': user_form, 'entreprise_form': entreprise_form})

# connexion entreprise    
def connexion_entreprise(request):
    if request.method == 'POST':
        # Récupère le formulaire de connexion personnalisé (email, mot de passe).
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            # Authentifie l'utilisateur et le connecte.
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profil_entreprise')
    else:
        form = AuthenticationForm()
    return render(request, 'entreprises/connexion_entreprise.html', {'form': form})

## vue d'accueil entreprise
@login_required
def profil_entreprise(request):
    # Cette vue affiche le profil de l'entreprise actuellement connectée.
    # Récupère l'utilisateur connecté à partir de l'objet "request".
    user = request.user
    # Récupère le profil d'entreprise associé à l'utilisateur connecté.
    entreprise = user.entreprise
    # Récupère les emplois publiés par l'entreprise.
    emplois = entreprise.emplois.all() 

    context = {
        'user': user,
        'entreprise': entreprise,
        'emplois': emplois,  
    }
    return render(request, 'entreprises/profil_entreprise.html', context)

# offre emploi en détails
def offre_emploi_detail(request, emploi_id):
    # Cette vue affiche les détails d'une offre d'emploi spécifique.
    emploi = get_object_or_404(Emploi, id=emploi_id)
    context = {'emploi': emploi}
    return render(request, 'emplois/offre_emploi_detail.html', context)    

# modifier offre par entreprise
@login_required
def modifier_offre(request, emploi_id):
    # Cette vue permet à l'entreprise de modifier une offre d'emploi.
    emploi = get_object_or_404(Emploi, id=emploi_id)

    if request.method == 'POST':
        # Récupère le formulaire de modification de l'offre d'emploi.
        form =  EmploiForm(request.POST, instance=emploi)
        if form.is_valid():
            form.save()
            return redirect('profil_entreprise')
    else:
        form =  EmploiForm(instance=emploi)

    context = {'form': form}
    return render(request, 'entreprises/modifier_offre.html', context)

## retirer l'offre par entreprise
@login_required
def retirer_offre(request, emploi_id):
    # Cette vue permet à l'entreprise de retirer une offre d'emploi.
    emploi = get_object_or_404(Emploi, id=emploi_id)
    if request.method == 'POST':
        emploi.delete()
        return redirect('profil_entreprise')
    return render(request, 'entreprises/retirer_offre.html', {'emploi': emploi})  

# rechercher emploi
def rechercher_emplois(request):
    # Cette vue permet à l'utilisateur de rechercher des emplois en fonction de différents critères.
    titre_poste = request.GET.get('titre_poste')
    ville = request.GET.get('ville')
    type_contrat = request.GET.get('type_contrat')
    domaine = request.GET.get('domaine')
    date_publication = request.GET.get('datePublication')
    
    emplois = Emploi.objects.all()
    
    if titre_poste:
        emplois = emplois.filter(titre__icontains=titre_poste)
    
    if ville:
        emplois = emplois.filter(ville__icontains=ville)
    
    if type_contrat:
        emplois = emplois.filter(type_contrat=type_contrat)
    
    if domaine:
        emplois = emplois.filter(domaine=domaine)
    
    if date_publication:
        emplois = emplois.filter(datePublication=date_publication)
    
    context = {
        'emplois': emplois
    }
    return render(request, 'home.html', context)  

# entreprise: modifier profil entreprise
@login_required
def modifier_profil_entreprise(request, entreprise_id):
    # Cette vue permet à l'entreprise de modifier son profil.
    user = request.user
    entreprise = user.entreprise
    entreprise = get_object_or_404(Entreprise, id=entreprise_id)

    if request.method == 'POST':
        # Récupère le formulaire de modification des informations de l'entreprise.
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            return redirect('profil_entreprise')
    else:
        form = EntrepriseForm(instance=entreprise)

    context = {
        'form': form
    }
    return render(request, 'entreprises/modifier_profil_entreprise.html', context)    

# Publier une offre d'emploi par entreprise
@login_required
def publier_offre_emploi(request):
    # Cette vue permet à l'entreprise de publier une nouvelle offre d'emploi.
    entreprise = Entreprise.objects.get(user=request.user)
    if request.method == 'POST':
        # Récupère le formulaire de publication d'offre d'emploi.
        form = EmploiForm(request.POST)
        if form.is_valid():
            emploi = form.save(commit=False)
            emploi.entreprise = entreprise
            emploi.save()
            return redirect('profil_entreprise')
    else:
        form = EmploiForm()
    return render(request, 'entreprises/publier_offre.html', {'form': form})

# Liste des candidatures reçues pour chaque entreprise
@login_required
def candidats_par_entreprise(request, entreprise_id):
    # Cette vue affiche la liste des candidats ayant postulé aux emplois publiés par une entreprise spécifique.
    entreprise = Entreprise.objects.get(id=entreprise_id)
    emplois = Emploi.objects.filter(entreprise=entreprise)
    emploi_ids = emplois.values_list('id', flat=True)
    candidats = Candidat.objects.filter(postuler__emploi_id__in=emploi_ids).distinct()

    context = {
        'entreprise_id': entreprise_id,
        'entreprise': entreprise,
        'emplois': emplois,
        'candidats': candidats,
        
    }

    return render(request, 'entreprises/candidats_par_entreprise.html', context)

# Modifier le statut d'une candidature par l'entreprise
def modifier_statut_candidature(request, postulation_id):
    # Cette vue permet à l'entreprise de modifier le statut d'une candidature.
    postulation = get_object_or_404(Postuler, id=postulation_id)

    if request.method == 'POST':
        # Récupère le formulaire de modification du statut de candidature.
        form = PostulerForm(instance=postulation, data=request.POST)
        if form.is_valid():
            ancien_statut = postulation.statutCandidature
            nouveau_statut = form.cleaned_data['statutCandidature']
            form.save()

            if ancien_statut != nouveau_statut:
                # Envoie une notification par e-mail au candidat en cas de changement de statut de candidature.
                sujet = "Mise à jour du statut de votre candidature"
                message = f"Bonjour {postulation.candidat},\n\nLe statut de votre candidature pour l'emploi {postulation.emploi} a été mis à jour. Le nouveau statut est : {nouveau_statut}.\n\nCordialement,\nL'équipe de l'entreprise."
                send_mail(sujet, message, settings.DEFAULT_FROM_EMAIL, [postulation.candidat.email])

            return redirect('candidats_par_entreprise', entreprise_id=postulation.emploi.entreprise_id)
    else:
        form = PostulerForm(instance=postulation)

    context = {
        'form': form,
        'postulation_id': postulation_id,
    }

    return render(request, 'entreprises/modifier_statut_candidature.html', context)

# Gestion du mot de passe oublié pour l'entreprise
# Définition d'une vue personnalisée pour la modification du mot de passe
class CustomPasswordChangeView(PasswordChangeView):
    # Utilisation du formulaire personnalisé pour le changement de mot de passe
    form_class = CustomSetPasswordForm

# Conversation entreprise et candidat
def chat_message(request, entreprise_id, candidat_id):
    # Cette vue gère la messagerie entre l'entreprise et le candidat.
    # Récupération des objets "entreprise" et "candidat" à partir de leurs IDs
    entreprise = get_object_or_404(User, id=entreprise_id)
    candidat = get_object_or_404(User, id=candidat_id)

    # Récupération de la conversation existante ou création d'une nouvelle conversation
    conversation, created = Conversation.objects.get_or_create(entreprise=entreprise, candidat=candidat)

    if request.method == 'POST':
        # Création du formulaire à partir des données de la requête
        form = MessageForm(request.POST)
        if form.is_valid():
            # Récupération du contenu du message depuis le formulaire valide
            contenu = form.cleaned_data['contenu']
            # Création d'un nouvel objet "Message" avec le contenu et l'expéditeur
            message = Message.objects.create(contenu=contenu, expediteur=request.user)
            # Ajout du message à la conversation
            conversation.messages.add(message)

            # Envoi de l'e-mail à l'autre utilisateur (entreprise ou candidat)
            # Sélection de l'adresse e-mail du destinataire en fonction de l'utilisateur actuel (expéditeur)
            destinataire = entreprise.email if request.user == candidat else candidat.email
            sujet = "Nouveau message dans la conversation"
            message_email = f"Bonjour,\n\nVous avez reçu un nouveau message dans votre conversation avec {request.user}.\n\nContenu du message : {contenu}\n\nCordialement,\nL'équipe de l'entreprise."
            # Envoi de l'e-mail avec les détails du message à la boîte de réception du destinataire
            send_mail(sujet, message_email, 'abakarhayar@gmail.com', [destinataire])

            # Redirection vers la vue de la conversation actuelle pour afficher le message nouvellement ajouté
            return redirect('chat_message', entreprise_id=entreprise_id, candidat_id=candidat_id)
    else:
        # Création d'un formulaire vide pour saisir le message si la méthode de requête est GET
        form = MessageForm()

    # Récupération de tous les messages de la conversation et tri par date
    messages = conversation.messages.all().order_by('date_message')

    context = {
        'entreprise': entreprise,
        'candidat': candidat,
        'messages': messages,
        'form': form
    }
    # Renvoi d'une réponse HTTP avec le template "chat_message.html" et un dictionnaire de contexte
    return render(request, 'message/chat_message.html', context)
