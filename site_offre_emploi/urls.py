"""site_offre_emploi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app.views import *
from django.contrib.auth.views import *
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('connexion_admin/', connexion_admin, name='connexion_admin'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('dashboard/', dashboard, name='dashboard'),
    path('supprimer_user/<int:user_id>/', supprimer_user, name='supprimer_user'),
    path('ajouter_user/', ajouter_user, name='ajouter_user'),
    path('modifier_user/<int:user_id>/', modifier_user, name='modifier_user'),
    path('ajouter_candidat/', ajouter_candidat, name='ajouter_candidat'),
    path('modifier_candidat/<int:candidat_id>/', modifier_candidat, name='modifier_candidat'),
    path('supprimer_candidat/<int:candidat_id>/', supprimer_candidat, name='supprimer_candidat'),
    path('ajouter_entreprise/', ajouter_entreprise, name='ajouter_entreprise'),
    path('modifier_entreprise/<int:entreprise_id>/', modifier_entreprise, name='modifier_entreprise'),
    path('supprimer_entreprise/<int:entreprise_id>/', supprimer_entreprise, name='supprimer_entreprise'),
    path('ajouter_emploi/', ajouter_emploi, name='ajouter_emploi'),
    path('modifier_emploi/<int:emploi_id>/', modifier_emploi, name='modifier_emploi'),
    path('supprimer_emploi/<int:emploi_id>/', supprimer_emploi, name='supprimer_emploi'),
    path('ajouter_postulation/', ajouter_postulation, name='ajouter_postulation'),
    path('modifier_postulation/<int:postulation_id>/', modifier_postulation, name='modifier_postulation'),
    path('supprimer_postulation/<int:postulation_id>/', supprimer_postulation, name='supprimer_postulation'),
    path('rechercher_emplois/', rechercher_emplois, name='rechercher_emplois'),
    path('ajouter_experience/', ajouter_experience, name='ajouter_experience'),
    path('modifier_experience/<int:experience_id>/', modifier_experience, name='modifier_experience'),
    path('supprimer_experience/<int:experience_id>/', supprimer_experience, name='supprimer_experience'),
    path('ajouter_competence/', ajouter_competence, name='ajouter_competence'),
    path('modifier_competence/<int:competence_id>/', modifier_competence, name='modifier_competence'),
    path('supprimer_competence/<int:competence_id>/', supprimer_competence, name='supprimer_competence'),
    path('ajouter_formation/', ajouter_formation, name='ajouter_formation'),
    path('modifier_formation/<int:formation_id>/', modifier_formation, name='modifier_formation'),
    path('supprimer_formation/<int:formation_id>/', supprimer_formation, name='supprimer_formation'),
    path('offre_emploi_detail/<int:emploi_id>/', offre_emploi_detail, name='offre_emploi_detail'),
    path('postuler_emploi/<int:emploi_id>/', postuler_emploi, name='postuler_emploi'),
    path('mes_candidatures/<int:candidat_id>/', mes_candidatures, name='mes_candidatures'),
    path('inscription_candidat/', inscription_candidat, name='inscription_candidat'),
    path('connexion_candidat/', connexion_candidat, name='connexion_candidat'),
    path('profil_candidat/', profil_candidat, name='profil_candidat'),
    path('modifier_profile_candidat/<int:candidat_id>', modifier_profile_candidat, name='modifier_profile_candidat'),
    path('ajouterCompetence/', ajouterCompetence, name='ajouterCompetence'),
    path('modifierCompetence/<int:competence_id>/', modifierCompetence, name='modifierCompetence'),
    path('supprimerCompetence/<int:competence_id>/', supprimerCompetence, name='supprimerCompetence'),
    path('ajouterExperience/', ajouterExperience, name='ajouterExperience'),
    path('modifierExperience/<int:experience_id>/', modifierExperience, name='modifierExperience'),
    path('supprimerExperience/<int:experience_id>/', supprimerExperience, name='supprimerExperience'),
    path('ajouterFormation/', ajouterFormation, name='ajouterFormation'),
    path('modifierFormation/<int:formation_id>/', modifierFormation, name='modifierFormation'),
    path('supprimerFormation/<int:formation_id>/', supprimerFormation, name='supprimerFormation'),
    path('inscription_entreprise/', inscription_entreprise, name='inscription_entreprise'),
    path('connexion_entreprise/', connexion_entreprise, name='connexion_entreprise'),
    path('profil_entreprise/', profil_entreprise, name='profil_entreprise'),
    path('modifier_profil_entreprise/<int:entreprise_id>', modifier_profil_entreprise, name='modifier_profil_entreprise'),
    path('publier_offre_emploi/', publier_offre_emploi, name='publier_offre_emploi'),
    path('modifier_offre/<int:emploi_id>/', modifier_offre, name='modifier_offre'),
    path('retirer_offre/<int:emploi_id>/', retirer_offre, name='retirer_offre'),
    path('candidats_par_entreprise/<int:entreprise_id>/', candidats_par_entreprise, name='candidats_par_entreprise'),
    path('modifier_statut_candidature/<int:postulation_id>/', modifier_statut_candidature, name='modifier_statut_candidature'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        form_class=CustomSetPasswordForm  # Utilisez votre formulaire personnalisé
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('chat_message/entreprise/<int:entreprise_id>/candidat/<int:candidat_id>/', chat_message, name='chat_message'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
