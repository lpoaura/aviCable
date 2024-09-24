-- TRUNCATE cables_app.cables_infrastructure RESTART IDENTITY CASCADE;
-- truncate cables_app.mortality_mortality restart IDENTITY cascade ;
-- IMPORT POINT

--
--
-- TRUNCATE cables_app.cables_infrastructure RESTART IDENTITY CASCADE;
-- TRUNCATE cables_app.mortality_mortality RESTART IDENTITY CASCADE;

ROLLBACK;

BEGIN;


ALTER TABLE ${schema_name}.t_inventaire_poteaux_erdf
    DROP COLUMN IF EXISTS uuid_action;
ALTER TABLE ${schema_name}.t_equipements_poteaux_erdf
    DROP COLUMN IF EXISTS uuid_action;
ALTER TABLE ${schema_name}.t_inventaire_troncons_erdf
    DROP COLUMN IF EXISTS uuid_action;
ALTER TABLE ${schema_name}.t_equipements_troncons_erdf
    DROP COLUMN IF EXISTS uuid_action;

ALTER TABLE ${schema_name}.t_inventaire_poteaux_erdf
    ADD COLUMN IF NOT EXISTS uuid_infstr UUID NOT NULL DEFAULT uuid_generate_v4();
ALTER TABLE ${schema_name}.t_inventaire_poteaux_erdf
    ADD COLUMN IF NOT EXISTS uuid_diagnosis UUID NOT NULL DEFAULT uuid_generate_v4();
ALTER TABLE ${schema_name}.t_equipements_poteaux_erdf
    ADD COLUMN IF NOT EXISTS uuid_operation UUID NOT NULL DEFAULT uuid_generate_v4();


ALTER TABLE ${schema_name}.t_inventaire_troncons_erdf
    ADD COLUMN IF NOT EXISTS uuid_infstr UUID NOT NULL DEFAULT uuid_generate_v4();
ALTER TABLE ${schema_name}.t_inventaire_troncons_erdf
    ADD COLUMN IF NOT EXISTS uuid_diagnosis UUID NOT NULL DEFAULT uuid_generate_v4();
ALTER TABLE ${schema_name}.t_equipements_troncons_erdf
    ADD COLUMN IF NOT EXISTS uuid_operation UUID NOT NULL DEFAULT uuid_generate_v4();


INSERT INTO cables_app.cables_infrastructure (timestamp_create, timestamp_update, uuid,
                                              created_by_id,
                                              owner_id,
                                              polymorphic_ctype_id, updated_by_id)
SELECT coalesce(date_inventaire, now()),
       now(),
       uuid_infstr,
       1,
       sinp_nomenclatures_nomenclature.id,
       django_content_type.id,
       1
FROM ${schema_name}.t_inventaire_poteaux_erdf
   , cables_app.sinp_nomenclatures_nomenclature
   , cables_app.django_content_type
WHERE code LIKE 'IO_ENEDIS'
  AND (django_content_type.app_label, django_content_type.model) = ('cables', 'point');

INSERT INTO cables_app.cables_point (infrastructure_ptr_id, geom)
SELECT cables_infrastructure.id, st_transform(geom, 4326) AS geom
FROM ${schema_name}.t_inventaire_poteaux_erdf
         JOIN cables_app.cables_infrastructure
              ON t_inventaire_poteaux_erdf.uuid_infstr = cables_infrastructure.uuid;

-- INSERT LINE


INSERT INTO cables_app.cables_infrastructure (timestamp_create, timestamp_update, uuid,
                                              created_by_id,
                                              owner_id,
                                              polymorphic_ctype_id, updated_by_id)
SELECT coalesce(date_inventaire, now()),
       now(),
       uuid_infstr,
       1,
       sinp_nomenclatures_nomenclature.id,
       django_content_type.id,
       1
FROM ${schema_name}.t_inventaire_troncons_erdf
   , cables_app.sinp_nomenclatures_nomenclature
   , cables_app.django_content_type
WHERE code LIKE 'IO_ENEDIS'
  AND (django_content_type.app_label, django_content_type.model) = ('cables', 'line');

INSERT INTO cables_app.cables_line (infrastructure_ptr_id, geom)
SELECT cables_infrastructure.id, st_transform(geom, 4326) AS geom
FROM ${schema_name}.t_inventaire_troncons_erdf
         JOIN cables_app.cables_infrastructure
              ON t_inventaire_troncons_erdf.uuid_infstr = cables_infrastructure.uuid;

-- COR AREAS


INSERT INTO cables_app.cables_infrastructure_geo_area (infrastructure_id, geoarea_id)
SELECT cables_infrastructure.id, geo_area.id
FROM cables_app.cables_infrastructure
         LEFT JOIN cables_app.cables_line
                   ON cables_infrastructure.id = cables_line.infrastructure_ptr_id
         LEFT JOIN cables_app.cables_point
                   ON cables_infrastructure.id = cables_point.infrastructure_ptr_id
         JOIN cables_app.geo_area
              ON st_intersects(coalesce(cables_line.geom, cables_point.geom), geo_area.geom)
ON CONFLICT DO NOTHING;

INSERT INTO cables_app.cables_diagnosis(timestamp_create, timestamp_update, uuid, date, remark, last, neutralized,
                                        isolation_advice, dissuasion_advice, attraction_advice, change_advice,
                                        technical_proposal, condition_id, created_by_id, infrastructure_id,
                                        pole_attractivity_id, pole_dangerousness_id, sgmt_build_integr_risk_id,
                                        sgmt_moving_risk_id, sgmt_topo_integr_risk_id, sgmt_veget_integr_risk_id,
                                        updated_by_id)
SELECT coalesce(date_inventaire, now())                  AS timestamp_create,
       now()                                             AS timestamp_update,
       t_inventaire_poteaux_erdf.uuid_diagnosis          AS uuid,
       coalesce(date_inventaire, '2000-01-01'::DATE)     AS date,
       remarques                                         AS remark,
       TRUE                                              AS last,
       coalesce(deja_neutralise, FALSE)                  AS neutralized,

       coalesce(neutralisation_prevue_isolation, FALSE)  AS isolation_advice,
       coalesce(neutralisation_prevue_dissuasion, FALSE) AS dissuasion_advice,
       coalesce(neutralisation_prevue_attraction, FALSE) AS attraction_advice,
       FALSE                                             AS change_advice,
       NULL                                              AS technical_proposal,
       6                                                 AS condition_id,
       1                                                 AS created_by_id,
       cables_infrastructure.id,
       pole_attractivity.id,
       pole_dangerosity.id,
       NULL                                              AS sgmt_build_integr_risk_id,
       NULL                                              AS sgmt_moving_risk_id,
       NULL                                              AS sgmt_topo_integr_risk_id,
       NULL                                              AS sgmt_veget_integr_risk_id,
       1                                                 AS updated_by_id
FROM ${schema_name}.t_inventaire_poteaux_erdf
         JOIN cables_app.cables_infrastructure ON t_inventaire_poteaux_erdf.uuid_infstr = cables_infrastructure.uuid
         LEFT JOIN ${schema_name}.dico_classes_risque AS attractivity
                   ON t_inventaire_poteaux_erdf.id_attractivite = attractivity.id_classe_risque
         LEFT JOIN cables_app.sinp_nomenclatures_nomenclature AS pole_attractivity
                   ON attractivity.lib_classe_risque = pole_attractivity.label
         LEFT JOIN ${schema_name}.dico_classes_risque AS dangerosity
                   ON t_inventaire_poteaux_erdf.id_dangerosite = dangerosity.id_classe_risque
         LEFT JOIN cables_app.sinp_nomenclatures_nomenclature AS pole_dangerosity
                   ON dangerosity.lib_classe_risque = pole_dangerosity.label;
                  
INSERT INTO cables_app.cables_diagnosis(timestamp_create, timestamp_update, uuid, date, remark, last, 
                                        isolation_advice, dissuasion_advice, attraction_advice, change_advice,
                                        technical_proposal, created_by_id, infrastructure_id,
                                        pole_attractivity_id, pole_dangerousness_id, sgmt_build_integr_risk_id,
                                        sgmt_moving_risk_id, sgmt_topo_integr_risk_id, sgmt_veget_integr_risk_id,
                                        updated_by_id)
select
	coalesce(date_inventaire,
	now()) as timestamp_create,
	now() as timestamp_update,
	t_inventaire_troncons_erdf.uuid_diagnosis as uuid,
	coalesce(date_inventaire,
	'2000-01-01'::DATE) as date,
	remarques as remark,
	true as last,
	false as isolation_advice,
	false as dissuasion_advice,
	false as attraction_advice,
	false as change_advice,
	'' as technical_proposal,
	1 as created_by_id,
	null::int,
	null::int,
	null::int,
	null as sgmt_build_integr_risk_id,
	nom_dep_risk.id as sgmt_moving_risk_id,
	nom_topo_risk.id as sgmt_topo_integr_risk_id,
	null as sgmt_veget_integr_risk_id,
	1 as updated_by_id
from
	cables74.t_inventaire_troncons_erdf
join cables_app.cables_infrastructure on
	t_inventaire_troncons_erdf.uuid_infstr = cables_infrastructure.uuid
left join cables74.dico_classes_risque as dep_risk
                   on
	t_inventaire_troncons_erdf.id_risque_deplacement = dep_risk.id_classe_risque
left join cables_app.sinp_nomenclatures_nomenclature as nom_dep_risk
                   on
	dep_risk.lib_classe_risque = nom_dep_risk.label
left join cables74.dico_classes_risque as topo_risk
                   on
	t_inventaire_troncons_erdf.id_risque_integration_topo = topo_risk.id_classe_risque
left join cables_app.sinp_nomenclatures_nomenclature as nom_topo_risk
                   on
	topo_risk.lib_classe_risque = nom_topo_risk.label;



--
-- CREATE TABLE tmp.species_from_olddbs AS
-- WITH list AS (SELECT DISTINCT nom_espece, COUNT(*) AS count
--               FROM ${schema_name}.t_especes
--                        JOIN ${schema_name}.t_cas_mortalite ON t_especes.id_espece = t_cas_mortalite.id_espece
--               GROUP BY nom_espece
--               UNION
--               SELECT DISTINCT nom_espece, COUNT(*)
--               FROM ${schema_name}.t_especes
--                        JOIN ${schema_name}.t_cas_mortalite ON t_especes.id_espece = t_cas_mortalite.id_espece
--               GROUP BY nom_espece
--               UNION
--               SELECT DISTINCT nom_espece, COUNT(*)
--               FROM ${schema_name}.t_especes
--                        JOIN ${schema_name}.t_cas_mortalite ON t_especes.id_espece = t_cas_mortalite.id_espece
--               GROUP BY nom_espece
--               UNION
--               SELECT DISTINCT nom_espece, COUNT(*)
--               FROM ${schema_name}.t_especes
--                        JOIN ${schema_name}.t_cas_mortalite ON t_especes.id_espece = t_cas_mortalite.id_espece
--               GROUP BY nom_espece
--               UNION
--               SELECT DISTINCT nom_espece, COUNT(*)
--               FROM ${schema_name}.t_especes
--                        JOIN ${schema_name}.t_cas_mortalite ON t_especes.id_espece = t_cas_mortalite.id_espece
--               GROUP BY nom_espece)
-- SELECT DISTINCT nom_espece, SUM(count), species_species.code AS cd_nom
-- FROM list
--          LEFT JOIN cables_app.species_species
--                    ON unaccent(LOWER(TRIM(SPLIT_PART(species_species.vernacular_name, '-', 1)))) =
--                       LOWER(unaccent(nom_espece))
-- GROUP BY nom_espece, cd_nom;

--
-- SELECT *
-- FROM ${schema_name}.t_especes;
--
-- SELECT *
-- FROM ${schema_name}.t_cas_mortalite
--          JOIN;
--
-- SELECT *
-- FROM ${schema_name}.dico_cause_mortalite;
--
-- SELECT *
-- FROM cables_app.sinp_nomenclatures_nomenclature
-- WHERE type_id = 9;

-- INSERT OPERATIONS

-- POINT OPERATIONS

INSERT INTO cables_app.cables_operation(timestamp_create, timestamp_update, uuid, date, remark, last, created_by_id,
                                        infrastructure_id, polymorphic_ctype_id, updated_by_id)
SELECT coalesce(date_equipement, now())              AS timestamp_create,
       now()                                         AS timestamp_update,
       t_equipements_poteaux_erdf.uuid_operation     AS uuid,
       coalesce(date_equipement, '2000-01-01'::DATE) AS date,
       NULL                                          AS remark,
       TRUE                                          AS last,
       1                                             AS created_by_id,
       cables_infrastructure.id                      AS infrastructure_id,
       django_content_type.id                        AS polymorphic_ctype_id,
       1                                             AS updated_by_id
FROM ${schema_name}.t_equipements_poteaux_erdf
         JOIN ${schema_name}.t_inventaire_poteaux_erdf ON t_equipements_poteaux_erdf.id_inventaire_poteau_erdf =
                                                          t_inventaire_poteaux_erdf.id_inventaire_poteau_erdf
         JOIN cables_app.cables_infrastructure
              ON t_inventaire_poteaux_erdf.uuid_infstr = cables_infrastructure.uuid
   , cables_app.django_content_type
  WHERE (django_content_type.app_label, django_content_type.model) = ('cables', 'pointoperation')
;

INSERT INTO cables_app.cables_equipment (uuid, timestamp_create, timestamp_update, count, reference, comment,
                                         created_by_id,
                                         type_id, updated_by_id)
--     (timestamp_create, timestamp_update, count, reference, comment, created_by_id, type_id, updated_by_id)
SELECT uuid_generate_v4()                 AS uuid,
       cables_operation.date              AS timestamp_create,
       cables_operation.date              AS timestamp_update,
       coalesce(id_nb_equipements, 0)     AS count,
       NULL                               AS reference,
       NULL                               AS comment,
       1                                  AS created_by_id,
       sinp_nomenclatures_nomenclature.id AS type_id,
       1                                  AS updated_by_id
FROM cables_app.cables_operation
         JOIN ${schema_name}.t_equipements_poteaux_erdf ON uuid_operation = cables_operation.uuid
         JOIN ${schema_name}.dico_type_equipement_poteau ON t_equipements_poteaux_erdf.id_type_equipement_poteau =
                                                            dico_type_equipement_poteau.id_type_equipement_poteau
         JOIN tmp.equipement_poteau ON dico_type_equipement_poteau.id_type_equipement_poteau = equipement_poteau.id
         JOIN cables_app.sinp_nomenclatures_nomenclature
              ON equipement_poteau.final_code = sinp_nomenclatures_nomenclature.code AND type_id = 7;


INSERT INTO cables_app.cables_pointoperation (operation_ptr_id, geom)
SELECT cables_operation.id, cables_point.geom
FROM cables_app.cables_operation
         JOIN ${schema_name}.t_equipements_poteaux_erdf ON uuid_operation = cables_operation.uuid
         JOIN cables_app.cables_infrastructure ON cables_operation.infrastructure_id = cables_infrastructure.id
         JOIN cables_app.cables_point ON cables_infrastructure.id = cables_point.infrastructure_ptr_id;

-- LINE OPERATIONS

INSERT INTO cables_app.cables_operation(timestamp_create, timestamp_update, uuid, date, remark, last, created_by_id,
                                        infrastructure_id, polymorphic_ctype_id, updated_by_id)
SELECT coalesce(t_equipements_troncons_erdf.date_equipement_troncon, now())              AS timestamp_create,
       now()                                                                             AS timestamp_update,
       t_equipements_troncons_erdf.uuid_operation                                        AS uuid,
       coalesce(t_equipements_troncons_erdf.date_equipement_troncon, '2000-01-01'::DATE) AS date,
       NULL                                                                              AS remark,
       TRUE                                                                              AS last,
       1                                                                                 AS created_by_id,
       cables_infrastructure.id                                                          AS infrastructure_id,
       django_content_type.id                                                            AS polymorphic_ctype_id,
       1                                                                                 AS updated_by_id
FROM ${schema_name}.t_equipements_troncons_erdf
         JOIN ${schema_name}.t_inventaire_troncons_erdf ON t_equipements_troncons_erdf.id_inventaire_troncon_erdf =
                                                           t_inventaire_troncons_erdf.id_inventaire_troncon_erdf
         JOIN cables_app.cables_infrastructure
              ON t_inventaire_troncons_erdf.uuid_infstr = cables_infrastructure.uuid
   , cables_app.django_content_type
WHERE (django_content_type.app_label, django_content_type.model) = ('cables', 'lineoperation')
;

INSERT INTO cables_app.cables_equipment (uuid, timestamp_create, timestamp_update, count, reference, comment,
                                         created_by_id,
                                         type_id, updated_by_id)
--     (timestamp_create, timestamp_update, count, reference, comment, created_by_id, type_id, updated_by_id)
SELECT uuid_generate_v4()                 AS uuid,
       cables_operation.date              AS timestamp_create,
       cables_operation.date              AS timestamp_update,
       0                                  AS count,
       NULL                               AS reference,
       NULL                               AS comment,
       1                                  AS created_by_id,
       sinp_nomenclatures_nomenclature.id AS type_id,
       1                                  AS updated_by_id
FROM cables_app.cables_operation
         JOIN ${schema_name}.t_equipements_troncons_erdf ON uuid_operation = cables_operation.uuid
         JOIN ${schema_name}.dico_type_equipement_troncon ON t_equipements_troncons_erdf.id_type_equipement_troncon =
                                                             dico_type_equipement_troncon.id_type_equipement_troncon
         JOIN tmp.equipement_troncon ON dico_type_equipement_troncon.id_type_equipement_troncon = equipement_troncon.id
         JOIN cables_app.sinp_nomenclatures_nomenclature
              ON equipement_troncon.final_code = sinp_nomenclatures_nomenclature.code AND type_id = 7;

--
INSERT INTO cables_app.cables_lineoperation (operation_ptr_id, geom)
SELECT cables_operation.id, t_equipements_troncons_erdf.geom
FROM cables_app.cables_operation
         JOIN ${schema_name}.t_equipements_troncons_erdf ON uuid_operation = cables_operation.uuid
;
-- INFO: MORTALITY DATA

WITH data AS (SELECT t_especes.nom_espece,
                     species_from_olddbs.cd_nom,
                     coalesce(date, '1900-01-01') AS date,
                     t_cas_mortalite.geom,
                     t_cas_mortalite.nb_cas,
                     t_cas_mortalite.source,
                     CASE
                         WHEN id_cause_mortalite = 1 THEN 'COD_EL'
                         WHEN id_cause_mortalite = 2 THEN 'COD_IM'
                         ELSE 'COD_UNKNOWN' END   AS death_cause
              FROM ${schema_name}.t_cas_mortalite
                       JOIN ${schema_name}.t_especes ON t_especes.id_espece = t_cas_mortalite.id_espece
                       JOIN tmp.species_from_olddbs
                            ON t_especes.nom_espece = species_from_olddbs.nom_espece
                       LEFT JOIN cables_app.species_species ON code = cd_nom)
INSERT
INTO cables_app.mortality_mortality(timestamp_create, timestamp_update, author, geom, date,
                                    nb_death,
                                    created_by_id,
                                    data_source_id, death_cause_id, infrstr_id, species_id,
                                    updated_by_id)
SELECT date,
       now(),
       1,
       st_transform(geom, 4326),
       date,
       coalesce(nb_cas, 1),
       1,
       NULL,
       nom_dc.id,
       NULL,
       species_species.id,
       1
FROM data
         JOIN cables_app.sinp_nomenclatures_nomenclature nom_dc ON death_cause = nom_dc.code
         JOIN cables_app.species_species ON data.cd_nom = species_species.code
ORDER BY date DESC;

COMMIT;
