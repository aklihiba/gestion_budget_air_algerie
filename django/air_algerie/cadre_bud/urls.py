from django.urls import path

from .views import *

urlpatterns = [

    path('login/' , user_login , name='login'), 
    path('logout_page/' , logout_page , name='logout_page'), 
    path('pre_pre_proposition_budgetaire/' , pre_pre_proposition_budgetaire , name='pre_pre_proposition_budgetaire'),    
    path('pre_proposition_budgetaire/' , pre_proposition_budgetaire , name='pre_proposition_budgetaire'),    
    path('proposition_budgetaire/' , proposition_budgetaire , name='proposition_budgetaire'),    
    path('proposition_trafic/' , proposition_trafic , name='proposition_trafic'),    
    path('proposition_recette/' , proposition_recette , name='proposition_recette'),    
    path('proposition_emission/' , proposition_emission , name='proposition_emission'), 
    path('proposition_depense/' , proposition_depense , name='proposition_depense'), 
    path('proposition_fonctionnement/' , proposition_fonctionnement1 , name='proposition_fonctionnement'),       
    path('proposition_exploitation/' , proposition_exploitation1 , name='proposition_exploitation'),       
      
    path('test/',test,name="test"),
    path('test1/',test1,name="test1"),
    path('test2/',test2,name="test2"),
    path('test3/',test3,name="test3"),
    path('consultation_proposition/' , consultation_proposition , name='consultation_proposition'),       
    path('pv_proposition/' , pv_proposition , name='pv_proposition'),     
  



    path('pre_pre_reunion_budgetaire/' , pre_pre_reunion_budgetaire , name='pre_pre_reunion_budgetaire'),    
    path('reunion_budgetaire/' , reunion_budgetaire , name='reunion_budgetaire'),  
    path('reunion_trafic/' , reunion_trafic , name='reunion_trafic'),    
    path('reunion_recette/' , reunion_recette , name='reunion_recette'),    
    path('reunion_emission/' , reunion_emission , name='reunion_emission'),    
    path('reunion_depenses/' , reunion_depenses1 , name='reunion_depenses'),  
    path('add_trafic_reunion/' , add_trafic_reunion , name='add_trafic_reunion'),   
    path('reunion_depenses1/' , reunion_depenses1 , name='reunion_depenses1'),    
 
  
   

  



 
    path('pre_pre_controle_budgetaire/' , pre_pre_controle_budgetaire , name='pre_pre_controle_budgetaire'),    
    path('pre_controle_budgetaire/' , pre_controle_budgetaire , name='pre_controle_budgetaire'),    
    path('controle_budgetaire/' , controle_budgetaire , name='controle_budgetaire'),    
    path('controle_trafic/' , controle_trafic , name='controle_trafic'),  
    path('controle_recette/' , controle_recette , name='controle_recette'),    
    path('controle_emission/' , controle_emission , name='controle_emission'),    
    path('controle_depense/' , controle_depense , name='controle_depense'),    
    path('controle_depense2/' , controle_depense2 , name='controle_depense2'),    
   

    path('add_controle_trafic/' , add_controle_trafic, name='add_controle_trafic'), 
    path('add_controle_recette/' , add_controle_recette, name='add_controle_recette'),    
    path('add_controle_emission/' , add_controle_emission, name='add_controle_emission'),    
    path('add_controle_depense/' , add_controle_depense, name='add_controle_depense'),    
    path('verifier_trafic/',verifier_trafic,name="verifier_trafic"),
    path('verifier_recette/',verifier_recette,name="verifier_recette"),
    path('verifier_emission/',verifier_emission,name="verifier_emission"),
    path('verifier_depenses/',verifier_depenses,name="verifier_depenses"),





    path('add_control/' , add_control , name='add_control'),   
    path('islam/',islam, name="islam"),
    path('mus/',mus, name="mus"),
    path('massi/',massi, name="massi"),
    path('ania/',ania, name="ania"),
    path('prt_depense/',prt_depense, name="prt_depense"),
    path('unite_notifie/',unite_notifie,name="unite_notifie"),
    path('consulter_notifie/',consulter_notifie,name="consulter_notifie"),
    path('pv_notifie/',pv_notifie,name="pv_notifie"),
    path('edit_trafic_proposition/',edit_trafic_proposition,name="edit_trafic_proposition"),
    path('update_trafic_proposition/',update_trafic_proposition,name="update_trafic_proposition"),
    path('edit_recette_proposition/',edit_recette_proposition,name="edit_recette_proposition"),
    path('update_recette_proposition/',update_recette_proposition,name="update_recette_proposition"),
    path('edit_emission_proposition/',edit_emission_proposition,name="edit_emission_proposition"),
    path('update_emission_proposition/',update_emission_proposition,name="update_emission_proposition"),
    path('edit_fonctionnement_proposition/',edit_fonctionnement_proposition,name="edit_fonctionnement_proposition"),
    path('update_fonctionnement_proposition/',update_fonctionnement_proposition,name="update_fonctionnement_proposition"),
    path('edit_exploitation_proposition/',edit_exploitation_proposition,name="edit_exploitation_proposition"),
    path('update_exploitation_proposition/',update_exploitation_proposition,name="update_exploitation_proposition"),
    path('get_mounth_controle/',get_mounth_controle,name="get_mounth_controle"),
    path('edit_mounth_controle/',edit_mounth_controle,name="edit_mounth_controle"),
    path('update_controle_trafic/',update_controle_trafic,name="update_controle_trafic"),
    path('update_controle_recette/',update_controle_recette,name="update_controle_recette"),
    path('edit_controle_recette/',edit_controle_recette,name="edit_controle_recette"),
    path('edit_controle_emission/',edit_controle_emission,name="edit_controle_emission"),
    path('update_controle_emission/',update_controle_emission,name="update_controle_emission"),
    path('edit_controle_fonctionnement/',edit_controle_fonctionnement,name="edit_controle_fonctionnement"),
    path('update_controle_fonctionnement/',update_controle_fonctionnement,name="update_controle_fonctionnement"),
    path('add_controle_depense2/',add_controle_depense2,name="add_controle_depense2"),
    path('edit_controle_exploitation/',edit_controle_exploitation,name="edit_controle_exploitation"),
    path('update_controle_exploitation/',update_controle_exploitation,name="update_controle_exploitation"),


    path('pv_notifie_m/',pv_notifie_m,name="pv_notifie_m"),

    path('consulter_controle/',consulter_controle,name="consulter_controle"),

    path('pre_consulter_controle/',pre_consulter_controle,name="pre_consulter_controle"),

    path('actualisation_consulter/',actualisation_consulter,name="actualisation_consulter"),
    path('actualisation_trafic/',actualisation_trafic,name="actualisation_trafic"),
    path('actualisation_recette/',actualisation_recette,name="actualisation_recette"),
    path('actualisation_emission/',actualisation_emission,name="actualisation_emission"),
    path('actualisation_depense/',actualisation_depense,name="actualisation_depense"),
    path('actualisation_unite/',actualisation_unite,name="actualisation_unite"),


    
    path('realisation_consulter/',realisation_consulter,name="realisation_consulter"),
    path('realisation_trafic/',realisation_trafic,name="realisation_trafic"),
    path('realisation_recette/',realisation_recette,name="realisation_recette"),
    path('realisation_emission/',realisation_emission,name="realisation_emission"),
    path('realisation_depense/',realisation_depense,name="realisation_depense"),
    path('realisation_unite/',realisation_unite,name="realisation_unite"),
    path('realisation_budgetaire/',realisation_budgetaire,name="realisation_budgetaire"),
    path('realisation_fonctionnement/',realisation_fonctionnement,name="realisation_fonctionnement"),
    path('realisation_exploitation/',realisation_exploitation,name="realisation_exploitation"),




    path('edit_fonctionnement_realisation/',edit_fonctionnement_realisation,name="edit_fonctionnement_realisation"),
    path('edit_exploitation_realisation/',edit_exploitation_realisation,name="edit_exploitation_realisation"),
    path('edit_emission_realisation/',edit_emission_realisation,name="edit_emission_realisation"),
    path('edit_recette_realisation/',edit_recette_realisation,name="edit_recette_realisation"),
    path('edit_trafic_realisation/',edit_trafic_realisation,name="edit_trafic_realisation"),
    path('update_trafic_realisation/',update_trafic_realisation,name="update_trafic_realisation"),
    path('update_recette_realisation/',update_recette_realisation,name="update_recette_realisation"),
    path('update_emission_realisation/',update_emission_realisation,name="update_emission_realisation"),
    path('update_fonctionnement_realisation/',update_fonctionnement_realisation,name="update_fonctionnement_realisation"),
    path('update_exploitation_realisation/',update_exploitation_realisation,name="update_exploitation_realisation"),
    path('pre_realisation/',pre_realisation,name="pre_realisation"),
    path('pre_traitement_realisation/',pre_traitement_realisation,name="pre_traitement_realisation"),
    path('add_realisation_trafic/',add_realisation_trafic,name="add_realisation_trafic"),
    path('add_realisation_recette/',add_realisation_recette,name="add_realisation_recette"),
    path('add_realisation_emission/',add_realisation_emission,name="add_realisation_emission"),
    path('add_realisation_fonctionnement/',add_realisation_fonctionnement,name="add_realisation_fonctionnement"),
    path('add_realisation_exploitation/',add_realisation_exploitation,name="add_realisation_exploitation"),
    path('pre_consulter_notifier/',pre_consulter_notifier,name="pre_consulter_notifier"),
    path('notifie_trafic/',notifie_trafic,name="notifie_trafic"),
    path('verifier_n_trafic/',verifier_n_trafic,name="verifier_n_trafic"),
    path('modifier_n_trafic/',modifier_n_trafic,name="modifier_n_trafic"),

    path('notifie_recette/',notifie_recette,name="notifie_recette"),
    path('verifier_n_recette/',verifier_n_recette,name="verifier_n_recette"),
    path('modifier_n_recette/',modifier_n_recette,name="modifier_n_recette"),

    path('notifie_emission/',notifie_emission,name="notifie_emission"),
    path('verifier_n_emission/',verifier_n_emission,name="verifier_n_emission"),
    path('modifier_n_emission/',modifier_n_emission,name="modifier_n_emission"),

    path('notifie_depenses/',notifie_depenses,name="notifie_depenses"),
    path('verifier_n_depenses/',verifier_n_depenses,name="verifier_n_depenses"),
    path('modifier_n_depenses/',modifier_n_depenses,name="modifier_n_depenses"),
    path('notifie_trafic_m/',notifie_trafic_m,name="notifie_trafic_m"),
    path('add_notifie_m/',add_notifie_m,name="add_notifie_m"),
    path('intermed_pv_proposition/',intermed_pv_proposition,name="intermed_pv_proposition"),
    path('massivn/',massivn,name="massivn"),
    path('islamvn/',islamvn,name="islamvn"),
    path('massivn1/',massivn1,name="massivn1"),
    path('islamvn1/',islamvn1,name="islamvn1"),
    path('musvn/',musvn,name="musvn"),

    path('intermed_pv_realisation/',intermed_pv_realisation,name="intermed_pv_realisation"),
    path('pv_realisation/',pv_realisation,name="pv_realisation"),
    path('pre_consulter_actualisation/',pre_consulter_actualisation,name="pre_consulter_actualisation"),
    path('pv_actualisation/',pv_actualisation,name="pv_actualisation"),
    path('modifier_a_trafic/',modifier_a_trafic,name="modifier_a_trafic"),
    path('verifier_a_trafic/',verifier_a_trafic,name="verifier_a_trafic"),

    path('reajustement_unite/',reajustement_unite,name="reajustement_unite"),
    path('pre_consulter_reajustement/',pre_consulter_reajustement,name="pre_consulter_reajustement"),
    path('pv_reajustement/',pv_reajustement,name="pv_reajustement"),
    path('reajustement_consulter/',reajustement_consulter,name="reajustement_consulter"),
    path('reajustement_trafic/',reajustement_trafic,name="reajustement_trafic"),
    path('verifier_r_trafic/',verifier_r_trafic,name="verifier_r_trafic"),
    path('modifier_r_trafic/',modifier_r_trafic,name="modifier_r_trafic"),

    path('verifier_a_recette/',verifier_a_recette,name="verifier_a_recette"),
    path('modifier_a_recette/',modifier_a_recette,name="modifier_a_recette"),

    path('verifier_a_emission/',verifier_a_emission,name="verifier_a_emission"),
    path('modifier_a_emission/',modifier_a_emission,name="modifier_a_emission"),

    path('verifier_a_depense/',verifier_a_depense,name="verifier_a_depense"),
    path('modifier_a_depense/',modifier_a_depense,name="modifier_a_depense"),
    

    path('reajustement_recette/',reajustement_recette,name="reajustement_recette"),
    path('verifier_r_recette/',verifier_r_recette,name="verifier_r_recette"),
    path('modifier_r_recette/',modifier_r_recette,name="modifier_r_recette"),
    

    path('reajustement_emission/',reajustement_emission,name="reajustement_emission"),
    path('verifier_r_emission/',verifier_r_emission,name="verifier_r_emission"),
    path('modifier_r_emission/',modifier_r_emission,name="modifier_r_emission"),


    path('reajustement_depense/',reajustement_depense,name="reajustement_depense"),
    path('verifier_r_depense/',verifier_r_depense,name="verifier_r_depense"),
    path('modifier_r_depense/',modifier_r_depense,name="modifier_r_depense"),




    path('pv_actualisation_m/',pv_actualisation_m,name="pv_actualisation_m"),
    path('actualisation_trafic_m/',actualisation_trafic_m,name="actualisation_trafic_m"),
    path('actualisation_recette_m/',actualisation_recette_m,name="actualisation_recette_m"),
    path('actualisation_emission_m/',actualisation_emission_m,name="actualisation_emission_m"),
    path('actualisation_depenses_m/',actualisation_depenses_m,name="actualisation_depenses_m"),




    path('notifie_recette_m/',notifie_recette_m,name="notifie_recette_m"),
    path('notifie_emission_m/',notifie_emission_m,name="notifie_emission_m"),
    path('notifie_depenses_m/',notifie_depenses_m,name="notifie_depenses_m"),




    path('pv_reajustement_m/',pv_reajustement_m,name="pv_reajustement_m"),
    path('reajustement_trafic_m/',reajustement_trafic_m,name="reajustement_trafic_m"),
    path('reajustement_recette_m/',reajustement_recette_m,name="reajustement_recette_m"),
    path('reajustement_emission_m/',reajustement_emission_m,name="reajustement_emission_m"),
    path('reajustement_depenses_m/',reajustement_depenses_m,name="reajustement_depenses_m"),

    
    path('modifier_trafic_m/',modifier_trafic_m,name="modifier_trafic_m"),
    path('add_recette_m/',add_recette_m,name="add_recette_m"),
    path('modifier_recette_m/',modifier_recette_m,name="modifier_recette_m"),


    path('add_emission_m/',add_emission_m,name="add_emission_m"),
    path('modifier_emission_m/',modifier_emission_m,name="modifier_emission_m"),

    path('add_depenses_m/',add_depenses_m,name="add_depenses_m"),
    path('modifier_depenses_m/',modifier_depenses_m,name="modifier_depenses_m"),

    #### hiba  #####
    path('delete_unite_pos_fct/',delete_unite_pos_fct,name="delete_unite_pos_fct"),





]