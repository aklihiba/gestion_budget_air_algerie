from django.urls import path

from .views import *

urlpatterns = [

    path('admin_user/',admin_user,name="admin_user"),
    path('add_user/',add_user,name="add_user"),
    path('edit_user/',edit_user,name="edit_user"),
    path('inter_edit/',inter_edit,name="inter_edit"),
    path('delete_user/',delete_user,name="delete_user"),




    path('admin_unite/',admin_unite,name="admin_unite"),
    path('add_unite/',add_unite,name="add_unite"),
    path('edit_unite/',edit_unite,name="edit_unite"),
    path('edit_unite1/',edit_unite1,name="edit_unite1"),

    path('delete_unite/',delete_unite,name="delete_unite"),




    path('admin_compte/',admin_compte,name="admin_compte"),
    path('add_compte/',add_compte,name="add_compte"),
    path('add_pos1/',add_pos1,name="add_pos1"),
    path('add_pos2/',add_pos2,name="add_pos2"),
    path('add_pos3/',add_pos3,name="add_pos3"),
    path('add_pos6/',add_pos6,name="add_pos6"),
    path('add_pos7/',add_pos7,name="add_pos7"),
    path('delete_compte/',delete_compte,name="delete_compte"),









    path('admin_affectation/',admin_affectation,name="admin_affectation"),
    path('affectation_date_reunion/',affectation_date_reunion,name="affectation_date_reunion"),
    path('interu_edit/',interu_edit,name="interu_edit"),
    path('edit_compte/',edit_compte,name="edit_compte"),
    path('interc_edit/',interc_edit,name="interc_edit"),
    path('add_unite_user/',add_unite_user,name="add_unite_user"),
    path('delete_unite_user/',delete_unite_user,name="delete_unite_user"),
    path('delete_up/',delete_up,name="delete_up"),
    path('add_unite_pos/',add_unite_pos,name="add_unite_pos"),
    path('delete_unite_pos/',delete_unite_pos,name="delete_unite_pos"),
    path('delete_up_pos/',delete_up_pos,name="delete_up_pos"),


    path('ouvrir/',ouvrir,name="ouvrir"),
    path('fermer/',fermer,name="fermer"),










    ]