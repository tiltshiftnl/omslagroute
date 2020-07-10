# Generated by Django 2.2.10 on 2020-07-10 08:01

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0021_auto_20200708_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='field_restrictions',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[['id', 'id [ID]'], ['created', 'created [Initieel opgeslagen datum/tijd]'], ['saved', 'saved [Opgeslagen datum/tijd]'], ['saved_by', 'saved_by [Opgeslagen door]'], ['saved_form', 'saved_form [Formulier]'], ['client_first_name', 'client_first_name [Client voornaam]'], ['client_last_name', 'client_last_name [Client achternaam]'], ['geslacht', 'geslacht [Geslacht]'], ['geboortedatum', 'geboortedatum [Geboortedatum]'], ['emailadres', 'emailadres [E-mailadres]'], ['woningnet_nummer', 'woningnet_nummer [Woningnetnummer]'], ['woningnet_geldigheid', 'woningnet_geldigheid [Geldigheid woninget]'], ['centrale_toegang_naam', 'centrale_toegang_naam [Naam centrale toegang]'], ['jonger_dan_26', 'jonger_dan_26 [Plaatsing jonger dan 26 jaar]'], ['jonger_dan_26_plaatsing_project', 'jonger_dan_26_plaatsing_project [Plaatsing jonger project]'], ['jonger_dan_26_motivatie_contract_onbepaalde', 'jonger_dan_26_motivatie_contract_onbepaalde [Motivatie voor contract onbepaalde tijd jongere]'], ['partner_check', 'partner_check [Heeft de cliënt een partner?]'], ['partner_naam', 'partner_naam [Partner naam]'], ['partner_geboortedatum', 'partner_geboortedatum [Partner geboortedatum]'], ['partner_gehuwd', 'partner_gehuwd [Gehuwd?]'], ['partner_echtscheiding_rond', 'partner_echtscheiding_rond [Echtscheiding rond?]'], ['partner_woonsituatie', 'partner_woonsituatie [Woonsituatie partner]'], ['kinderen_check', 'kinderen_check [Heeft de cliënt kinderen?]'], ['kinderen', 'kinderen [Kinderen]'], ['centrale_toegang_trajectwijziging_ed', 'centrale_toegang_trajectwijziging_ed [Toegang en trajectwijziging / doorstroom en jeugdzorg]'], ['trajecthouder_naam', 'trajecthouder_naam [Naam instroomfunctionaris of trajecthouder]'], ['aanvraag_datum', 'aanvraag_datum [Datum aanvraag]'], ['omslagwoning_zorgaanbieder', 'omslagwoning_zorgaanbieder [Zorgaanbieder omslagwoning]'], ['urgentiecriteria_zinvolle_dagbesteding', 'urgentiecriteria_zinvolle_dagbesteding [De cliënt heeft passende zinvolle dagbesteding]'], ['urgentiecriteria_functioneert_sociaal_stabiel', 'urgentiecriteria_functioneert_sociaal_stabiel [De cliënt functioneert sociaal stabiel]'], ['urgentiecriteria_functioneert_psychisch_stabiel', 'urgentiecriteria_functioneert_psychisch_stabiel [De cliënt functioneert psychisch stabiel]'], ['urgentiecriteria_is_financieel_stabiel', 'urgentiecriteria_is_financieel_stabiel [De cliënt is financieel stabiel]'], ['urgentiecriteria_kinderen_gezonde_omgeving', 'urgentiecriteria_kinderen_gezonde_omgeving [De betrokken kinderen hebben een gezonde omgeving]'], ['medische_problemen_mbt_traplopen', 'medische_problemen_mbt_traplopen [Zijn er medische problemen m.b.t. traplopen?]'], ['medische_problemen_mbt_traplopen_check', 'medische_problemen_mbt_traplopen_check [Zijn er medische problemen m.b.t. traplopen?]'], ['medische_problemen_wooneisen', 'medische_problemen_wooneisen [Zo ja, benedenwoning of woning met lift? Anders?]'], ['medische_problemen_bewijslast', 'medische_problemen_bewijslast [Voeg medische gegevens toe m.b.t. problematiek]'], ['uitsluiting_stadsdeel_argumentatie', 'uitsluiting_stadsdeel_argumentatie [Uitsluiting stadsdeel, argumentatie]'], ['organisatie', 'organisatie [Organisatie]'], ['persoonlijk_begeleider', 'persoonlijk_begeleider [Persoonlijk begeleider]'], ['start_zelfstandig_wonen', 'start_zelfstandig_wonen [Start zelfstandig wonen (intermediair)]'], ['datum_voordracht', 'datum_voordracht [Datum voordracht]'], ['woningcorporatie_akkoord_met_omklap', 'woningcorporatie_akkoord_met_omklap [Woningcorporatie akkoord met omklap]'], ['datum_evaluatie_moment', 'datum_evaluatie_moment [Datum evaluatie moment]'], ['urgentiecriteria_zinvolle_dagbesteding_behaald_omdat', 'urgentiecriteria_zinvolle_dagbesteding_behaald_omdat [Deze doelen zijn behaald omdat]'], ['urgentiecriteria_zinvolle_dagbesteding_beoordeeld_door', 'urgentiecriteria_zinvolle_dagbesteding_beoordeeld_door [Deze doelen zijn beoordeeld door]'], ['urgentiecriteria_zinvolle_dagbesteding_akkoord', 'urgentiecriteria_zinvolle_dagbesteding_akkoord [Akkoord]'], ['urgentiecriteria_zinvolle_dagbesteding_datum_evaluatiemoment', 'urgentiecriteria_zinvolle_dagbesteding_datum_evaluatiemoment [Datum evaluatiemoment]'], ['urgentiecriteria_functioneert_sociaal_behaald_omdat', 'urgentiecriteria_functioneert_sociaal_behaald_omdat [Deze doelen zijn behaald omdat]'], ['urgentiecriteria_functioneert_sociaal_beoordeeld_door', 'urgentiecriteria_functioneert_sociaal_beoordeeld_door [Deze doelen zijn beoordeeld door]'], ['urgentiecriteria_functioneert_sociaal_akkoord', 'urgentiecriteria_functioneert_sociaal_akkoord [Akkoord]'], ['urgentiecriteria_functioneert_sociaal_datum_evaluatiemoment', 'urgentiecriteria_functioneert_sociaal_datum_evaluatiemoment [Datum evaluatiemoment]'], ['urgentiecriteria_functioneert_psychisch_behaald_omdat', 'urgentiecriteria_functioneert_psychisch_behaald_omdat [Deze doelen zijn behaald omdat]'], ['urgentiecriteria_functioneert_psychisch_beoordeeld_door', 'urgentiecriteria_functioneert_psychisch_beoordeeld_door [Deze doelen zijn beoordeeld door]'], ['urgentiecriteria_functioneert_psychisch_akkoord', 'urgentiecriteria_functioneert_psychisch_akkoord [Akkoord]'], ['urgentiecriteria_functioneert_psychisch_datum_evaluatiemoment', 'urgentiecriteria_functioneert_psychisch_datum_evaluatiemoment [Datum evaluatiemoment]'], ['urgentiecriteria_is_financieel_stabiel_behaald_omdat', 'urgentiecriteria_is_financieel_stabiel_behaald_omdat [Deze doelen zijn behaald omdat]'], ['urgentiecriteria_is_financieel_stabiel_beoordeeld_door', 'urgentiecriteria_is_financieel_stabiel_beoordeeld_door [Deze doelen zijn beoordeeld door]'], ['urgentiecriteria_is_financieel_stabiel_akkoord', 'urgentiecriteria_is_financieel_stabiel_akkoord [Akkoord]'], ['urgentiecriteria_is_financieel_stabiel_datum_evaluatiemoment', 'urgentiecriteria_is_financieel_stabiel_datum_evaluatiemoment [Datum evaluatiemoment]'], ['urgentiecriteria_kinderen_gezonde_behaald_omdat', 'urgentiecriteria_kinderen_gezonde_behaald_omdat [Deze doelen zijn behaald omdat]'], ['urgentiecriteria_kinderen_gezonde_beoordeeld_door', 'urgentiecriteria_kinderen_gezonde_beoordeeld_door [Deze doelen zijn beoordeeld door]'], ['urgentiecriteria_kinderen_gezonde_akkoord', 'urgentiecriteria_kinderen_gezonde_akkoord [Akkoord]'], ['urgentiecriteria_kinderen_gezonde_datum_evaluatiemoment', 'urgentiecriteria_kinderen_gezonde_datum_evaluatiemoment [Datum evaluatiemoment]'], ['omklap_client_openstaande_vragen', 'omklap_client_openstaande_vragen [Voor deze cliënt staan de volgende vragen nog open]'], ['omklap_client_volgende_stappen_gezet', 'omklap_client_volgende_stappen_gezet [Hiervoor worden de volgende stappen gezet (zowel formeel als informeel)]'], ['omklap_beoordeeld_door', 'omklap_beoordeeld_door [Dit is beoordeeld door]'], ['omklap_datum_evaluatiemoment', 'omklap_datum_evaluatiemoment [Datum evaluatiemoment]'], ['omklap_toelichting', 'omklap_toelichting [Toelichting (bv. doelen niet behaald maar geen risico voor zelfstandig wonen)]'], ['omklap_akkoord_derde', 'omklap_akkoord_derde [Akkoord objectieve derde]'], ['omklap_akkoord_derde_toelichting', 'omklap_akkoord_derde_toelichting [Toelichting]'], ['omklap_akkoord_derde_naam', 'omklap_akkoord_derde_naam [Naam / afdeling objectieve derde]'], ['omklap_akkoord_derde_datum', 'omklap_akkoord_derde_datum [Datum van akkoord]'], ['wonen_dossier_nr', 'wonen_dossier_nr [Dossier nr.]'], ['adres_straatnaam', 'adres_straatnaam [Straatnaam]'], ['adres_huisnummer', 'adres_huisnummer [Huisnummer]'], ['adres_toevoeging', 'adres_toevoeging [Toevoeging]'], ['adres_postcode', 'adres_postcode [Postcode]'], ['adres_plaatsnaam', 'adres_plaatsnaam [Plaatsnaam]'], ['adres_wijziging_reden', 'adres_wijziging_reden [Waarom wijzig je dit adres?]'], ['woningcorporatie', 'woningcorporatie [Woningcorporatie]'], ['woningcorporatie_medewerker', 'woningcorporatie_medewerker [Woningcorporatie medewerker]'], ['delete_request_date', 'delete_request_date [Verwijder verzoek datum]'], ['delete_request_by', 'delete_request_by [Verwijder verzoek door]'], ['delete_request_message', 'delete_request_message [Verwijder verzoek bericht]']], help_text='De inhoud van een geselecteerd veld wordt zichtbaar voor deze organisatie.', max_length=2541, null=True, verbose_name='Cliënt gegevens velden'),
        ),
    ]
