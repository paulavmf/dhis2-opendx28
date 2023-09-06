## Proyecto de parametrización de DHIS2 para OpenDX28


1. levantar los servicios wey db mediante docker compose up-d
2. ir a localhost:8080
3. entrar en el sistema usando usuario: admin contraseña:district
4. entrar en la aplicación Import/Export 
5. importar en formato JSON el fichero: metadatas/metadata_orgunits_level_group_groupset_attribute_users_export_11_07_23_.json
   (esimportante que este sea el primero en ser importado) este tambien tiene el superuser configurado para tener acceso a datasets, dashboards y unidades organizativas
6. importar en formato JSON el fichero: metadatas/IDS_AGG_1.2.0_DHIS2.39/IDS_AGG_COMPLETE_1.2.0_DHIS2.39/IDS_AGG_COMPLETE_1.2.0_DHIS2.39.json
este dicheeo ha sido modificado para hacer referencia a lo niveles de unidades organizativas tal como explica el la referencia de instalación, ver: metadatas/IDS_AGG_1.2.0_DHIS2.39/ids_agg-installation-v1.2.0.pdf
7. Por último importar el fichero metadatas/IDS_AGG_1.2.0_DHIS2.39/IDS_AGG_COMPLETE_DASHBOARD_1.2.0_DHIS2.39/IDS_AGG_COMPLETE_DASHBOARD_1.2.0_DHIS2.39.json



