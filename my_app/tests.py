from django.test import RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from my_app.views import dashboard  # Remplacez 'myapp' par le nom de votre application

import pytest

@pytest.mark.django_db
def test_dashboard_authenticated_superuser():
    # Créez un superutilisateur fictif pour le test
    user = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')

    # Utilisez la RequestFactory pour créer une requête GET pour la vue dashboard
    request = RequestFactory().get(reverse('dashboard'))  # Assurez-vous que 'dashboard' est le nom de l'URL associée à la vue

    # Associez l'utilisateur fictif à la requête
    request.user = user

    # Appelez la vue et récupérez la réponse
    response = dashboard(request)

    # Vérifiez que la réponse a un statut HTTP 200 (OK)
    assert response.status_code == 200

    # Vérifiez que la vue rend le bon template
    assert 'admin/dashboard.html' in [template.name for template in response.templates]

    # Vérifiez que le contexte contient les données attendues (vous pouvez ajuster cela en fonction de votre vue)
    assert 'candidats' in response.context
    assert 'entreprises' in response.context
    assert 'emplois' in response.context
    assert 'users' in response.context
    assert 'competences' in response.context
    assert 'formations' in response.context
    assert 'experiences' in response.context
    assert 'conversations' in response.context
    assert 'messages' in response.context
    assert 'postulations' in response.context

def test_dashboard_unauthenticated_user():
    # Utilisez la RequestFactory pour créer une requête GET pour la vue dashboard sans utilisateur authentifié
    request = RequestFactory().get(reverse('dashboard'))  # Assurez-vous que 'dashboard' est le nom de l'URL associée à la vue

    # Appelez la vue et récupérez la réponse
    response = dashboard(request)

    # Vérifiez que la réponse a un statut HTTP 200 (OK)
    assert response.status_code == 200

    # Vérifiez que la vue rend le bon template
    assert 'admin/dashboard.html' in [template.name for template in response.templates]

    # Vérifiez que la réponse contient le message "Accès refusé"
    assert "Accès refusé" in response.content.decode('utf-8')
from django.test import RequestFactory
from django.urls import reverse
from my_app.models import Emploi  # Importez le modèle Emploi (remplacez 'myapp' par le nom de votre application)
from my_app.views import home  # Importez la vue home (remplacez 'myapp' par le nom de votre application)

import pytest

@pytest.mark.django_db
def test_home_view():
    # Créez des objets Emploi fictifs pour le test
    emploi1 = Emploi.objects.create(titre='Emploi 1', description='Description de l\'emploi 1')
    emploi2 = Emploi.objects.create(titre='Emploi 2', description='Description de l\'emploi 2')

    # Utilisez la RequestFactory pour créer une requête GET pour la vue home
    request = RequestFactory().get(reverse('home'))  # Assurez-vous que 'home' est le nom de l'URL associée à la vue

    # Appelez la vue et récupérez la réponse
    response = home(request)

    # Vérifiez que la réponse a un statut HTTP 200 (OK)
    assert response.status_code == 200

    # Vérifiez que la vue rend le bon template
    assert 'home.html' in [template.name for template in response.templates]

    # Vérifiez que le contexte contient les données attendues (emplois)
    assert 'emplois' in response.context
    emplois_in_context = response.context['emplois']
    assert len(emplois_in_context) == 2  # Vérifiez que la liste des emplois contient les deux emplois fictifs créés
    assert emploi1 in emplois_in_context
    assert emploi2 in emplois_in_context
