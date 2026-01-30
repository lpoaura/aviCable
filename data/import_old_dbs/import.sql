-- TRUNCATE cables_app.cables_infrastructure RESTART IDENTITY CASCADE;
-- truncate cables_app.mortality_mortality restart IDENTITY cascade ;
-- IMPORT POINT
--
--
-- TRUNCATE cables_app.cables_infrastructure RESTART IDENTITY CASCADE;
-- TRUNCATE cables_app.mortality_mortality RESTART IDENTITY CASCADE;


begin;

create or replace
function array_greatest(anyarray)
returns anyelement language sql as $$
select
	max(x)
from
	unnest($1) as a(x);

$$;

alter table ${schema_name}.t_inventaire_poteaux_erdf
    drop column if exists uuid_action;

alter table ${schema_name}.t_equipements_poteaux_erdf
    drop column if exists uuid_action;

alter table ${schema_name}.t_inventaire_troncons_erdf
    drop column if exists uuid_action;

alter table ${schema_name}.t_equipements_troncons_erdf
    drop column if exists uuid_action;

alter table ${schema_name}.t_inventaire_poteaux_erdf
    add column if not exists uuid_infstr UUID not null default uuid_generate_v4();

alter table ${schema_name}.t_inventaire_poteaux_erdf
    add column if not exists uuid_diagnosis UUID not null default uuid_generate_v4();

alter table ${schema_name}.t_equipements_poteaux_erdf
    add column if not exists uuid_operation UUID not null default uuid_generate_v4();

alter table ${schema_name}.t_inventaire_troncons_erdf
    add column if not exists uuid_infstr UUID not null default uuid_generate_v4();

alter table ${schema_name}.t_inventaire_troncons_erdf
    add column if not exists uuid_diagnosis UUID not null default uuid_generate_v4();

alter table ${schema_name}.t_equipements_troncons_erdf
    add column if not exists uuid_operation UUID not null default uuid_generate_v4();

insert
	into
	cables_app.cables_infrastructure (timestamp_create,
	timestamp_update,
	uuid,
	created_by_id,
	owner_id,
	polymorphic_ctype_id,
	updated_by_id)
select
	coalesce(date_inventaire,
	now()),
	now(),
	uuid_infstr,
	1,
	sinp_nomenclatures_nomenclature.id,
	django_content_type.id,
	1
from
	${schema_name}.t_inventaire_poteaux_erdf
   ,
	cables_app.sinp_nomenclatures_nomenclature
   ,
	cables_app.django_content_type
where
	code like 'IO-ENEDIS'
	and (django_content_type.app_label,
	django_content_type.model) = ('cables',
	'point');

insert
	into
	cables_app.cables_point (infrastructure_ptr_id,
	geom)
select
	cables_infrastructure.id,
	st_transform(geom,
	4326) as geom
from
	${schema_name}.t_inventaire_poteaux_erdf
join cables_app.cables_infrastructure
              on
	t_inventaire_poteaux_erdf.uuid_infstr = cables_infrastructure.uuid;
-- INSERT LINE


insert
	into
	cables_app.cables_infrastructure (timestamp_create,
	timestamp_update,
	uuid,
	created_by_id,
	owner_id,
	polymorphic_ctype_id,
	updated_by_id)
select
	coalesce(date_inventaire,
	now()),
	now(),
	uuid_infstr,
	1,
	sinp_nomenclatures_nomenclature.id,
	django_content_type.id,
	1
from
	${schema_name}.t_inventaire_troncons_erdf
   ,
	cables_app.sinp_nomenclatures_nomenclature
   ,
	cables_app.django_content_type
where
	code like 'IO-ENEDIS'
	and (django_content_type.app_label,
	django_content_type.model) = ('cables',
	'line');

insert
	into
	cables_app.cables_line (infrastructure_ptr_id,
	geom)
select
	cables_infrastructure.id,
	st_transform(geom,
	4326) as geom
from
	${schema_name}.t_inventaire_troncons_erdf
join cables_app.cables_infrastructure
              on
	t_inventaire_troncons_erdf.uuid_infstr = cables_infrastructure.uuid;
-- COR AREAS


insert
	into
	cables_app.cables_infrastructure_areas (infrastructure_id,
	geoarea_id)
select
	cables_infrastructure.id,
	geo_area.id
from
	cables_app.cables_infrastructure
left join cables_app.cables_line
                   on
	cables_infrastructure.id = cables_line.infrastructure_ptr_id
left join cables_app.cables_point
                   on
	cables_infrastructure.id = cables_point.infrastructure_ptr_id
join cables_app.geo_area
              on
	st_intersects(coalesce(cables_line.geom,
	cables_point.geom),
	geo_area.geom)
on
	conflict do nothing;

insert
	into
	cables_app.cables_diagnosis(timestamp_create,
	timestamp_update,
	uuid,
	date,
	remark,
	last,
	isolation_advice,
	dissuasion_advice,
	attraction_advice,
	change_advice,
	technical_proposal,
	created_by_id,
	infrastructure_id,
	pole_attractivity_id,
	pole_dangerousness_id,
	sgmt_moving_risk_id,
	sgmt_topo_integr_risk_id,
	sgmt_landscape_integr_risk_id,
	updated_by_id)
select
	coalesce(date_inventaire,
	now()) as timestamp_create,
	now() as timestamp_update,
	t_inventaire_poteaux_erdf.uuid_diagnosis as uuid,
	coalesce(date_inventaire,
	'2000-01-01'::DATE) as date,
	remarques as remark,
	true as last,
	coalesce(neutralisation_prevue_isolation,
	false) as isolation_advice,
	coalesce(neutralisation_prevue_dissuasion,
	false) as dissuasion_advice,
	coalesce(neutralisation_prevue_attraction,
	false) as attraction_advice,
	false as change_advice,
	null as technical_proposal,
	1 as created_by_id,
	cables_infrastructure.id,
	pole_attractivity.id,
	pole_dangerosity.id,
	null as sgmt_moving_risk_id,
	null as sgmt_topo_integr_risk_id,
	null as sgmt_landscape_integr_risk_id,
	1 as updated_by_id
from
	${schema_name}.t_inventaire_poteaux_erdf
join cables_app.cables_infrastructure on
	t_inventaire_poteaux_erdf.uuid_infstr = cables_infrastructure.uuid
left join ${schema_name}.dico_classes_risque as attractivity
                   on
	t_inventaire_poteaux_erdf.id_attractivite = attractivity.id_classe_risque
left join cables_app.sinp_nomenclatures_nomenclature as pole_attractivity
                   on
	attractivity.lib_classe_risque = pole_attractivity.label
left join ${schema_name}.dico_classes_risque as dangerosity
                   on
	t_inventaire_poteaux_erdf.id_dangerosite = dangerosity.id_classe_risque
left join cables_app.sinp_nomenclatures_nomenclature as pole_dangerosity
                   on
	dangerosity.lib_classe_risque = pole_dangerosity.label;

insert
	into
	cables_app.cables_diagnosis(timestamp_create,
	timestamp_update,
	uuid,
	date,
	remark,
	last,
	isolation_advice,
	dissuasion_advice,
	attraction_advice,
	change_advice,
	technical_proposal,
	created_by_id,
	infrastructure_id,
	pole_attractivity_id,
	pole_dangerousness_id,
	sgmt_moving_risk_id,
	sgmt_topo_integr_risk_id,
	sgmt_landscape_integr_risk_id,
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
	cables_infrastructure.id as infrastructure_id,
	null::int as pole_attractivity_id,
	null::int as pole_dangerousness_id,
	nom_dep_risk.id as sgmt_moving_risk_id,
	nom_topo_risk.id as sgmt_topo_integr_risk_id,
	nom_landscape_risk.id as sgmt_veget_integr_risk_id,
	1 as updated_by_id
from
	${schema_name}.t_inventaire_troncons_erdf
join cables_app.cables_infrastructure on
	t_inventaire_troncons_erdf.uuid_infstr = cables_infrastructure.uuid
left join ${schema_name}.dico_classes_risque as dep_risk
                   on
	t_inventaire_troncons_erdf.id_risque_deplacement = dep_risk.id_classe_risque
left join cables_app.sinp_nomenclatures_nomenclature as nom_dep_risk
                   on
	dep_risk.lib_classe_risque = nom_dep_risk.label
left join ${schema_name}.dico_classes_risque as topo_risk
                   on
	t_inventaire_troncons_erdf.id_risque_integration_topo = topo_risk.id_classe_risque
left join cables_app.sinp_nomenclatures_nomenclature as nom_topo_risk
                   on
	topo_risk.lib_classe_risque = nom_topo_risk.label
left join ${schema_name}.dico_classes_risque as landscape_risk
                   on
	array_greatest(array[t_inventaire_troncons_erdf.id_risque_integration_bati,
	t_inventaire_troncons_erdf.id_risque_integration_vegetation]) = landscape_risk.id_classe_risque
left join cables_app.sinp_nomenclatures_nomenclature as nom_landscape_risk
                   on
	topo_risk.lib_classe_risque = nom_landscape_risk.label;
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

insert
	into
	cables_app.cables_operation(timestamp_create,
	timestamp_update,
	uuid,
	date,
	remark,
	last,
	created_by_id,
	infrastructure_id,
	polymorphic_ctype_id,
	updated_by_id)
select
	coalesce(date_equipement,
	now()) as timestamp_create,
	now() as timestamp_update,
	t_equipements_poteaux_erdf.uuid_operation as uuid,
	coalesce(date_equipement,
	'2000-01-01'::DATE) as date,
	null as remark,
	true as last,
	1 as created_by_id,
	cables_infrastructure.id as infrastructure_id,
	django_content_type.id as polymorphic_ctype_id,
	1 as updated_by_id
from
	${schema_name}.t_equipements_poteaux_erdf
join ${schema_name}.t_inventaire_poteaux_erdf on
	t_equipements_poteaux_erdf.id_inventaire_poteau_erdf =
                                                          t_inventaire_poteaux_erdf.id_inventaire_poteau_erdf
join cables_app.cables_infrastructure
              on
	t_inventaire_poteaux_erdf.uuid_infstr = cables_infrastructure.uuid
   ,
	cables_app.django_content_type
where
	(django_content_type.app_label,
	django_content_type.model) = ('cables',
	'pointoperation')
;

insert
	into
	cables_app.cables_equipment (uuid,
	timestamp_create,
	timestamp_update,
	count,
	reference,
	comment,
	created_by_id,
	type_id,
	updated_by_id)
	--     (timestamp_create, timestamp_update, count, reference, comment, created_by_id, type_id, updated_by_id)
select
	uuid_generate_v4() as uuid,
	cables_operation.date as timestamp_create,
	cables_operation.date as timestamp_update,
	coalesce(id_nb_equipements,
	0) as count,
	null as reference,
	null as comment,
	1 as created_by_id,
	sinp_nomenclatures_nomenclature.id as type_id,
	1 as updated_by_id
from
	cables_app.cables_operation
join ${schema_name}.t_equipements_poteaux_erdf on
	uuid_operation = cables_operation.uuid
join ${schema_name}.dico_type_equipement_poteau on
	t_equipements_poteaux_erdf.id_type_equipement_poteau =
                                                            dico_type_equipement_poteau.id_type_equipement_poteau
join tmp.equipement_poteau on
	dico_type_equipement_poteau.id_type_equipement_poteau = equipement_poteau.id
join cables_app.sinp_nomenclatures_nomenclature
              on
	equipement_poteau.final_code = sinp_nomenclatures_nomenclature.code
	and type_id = 7;

insert
	into
	cables_app.cables_pointoperation (operation_ptr_id,
	geom)
select
	cables_operation.id,
	cables_point.geom
from
	cables_app.cables_operation
join ${schema_name}.t_equipements_poteaux_erdf on
	uuid_operation = cables_operation.uuid
join cables_app.cables_infrastructure on
	cables_operation.infrastructure_id = cables_infrastructure.id
join cables_app.cables_point on
	cables_infrastructure.id = cables_point.infrastructure_ptr_id;
-- LINE OPERATIONS

insert
	into
	cables_app.cables_operation(timestamp_create,
	timestamp_update,
	uuid,
	date,
	remark,
	last,
	created_by_id,
	infrastructure_id,
	polymorphic_ctype_id,
	updated_by_id)
select
	coalesce(t_equipements_troncons_erdf.date_equipement_troncon,
	now()) as timestamp_create,
	now() as timestamp_update,
	t_equipements_troncons_erdf.uuid_operation as uuid,
	coalesce(t_equipements_troncons_erdf.date_equipement_troncon,
	'2000-01-01'::DATE) as date,
	null as remark,
	true as last,
	1 as created_by_id,
	cables_infrastructure.id as infrastructure_id,
	django_content_type.id as polymorphic_ctype_id,
	1 as updated_by_id
from
	${schema_name}.t_equipements_troncons_erdf
join ${schema_name}.t_inventaire_troncons_erdf on
	t_equipements_troncons_erdf.id_inventaire_troncon_erdf =
                                                           t_inventaire_troncons_erdf.id_inventaire_troncon_erdf
join cables_app.cables_infrastructure
              on
	t_inventaire_troncons_erdf.uuid_infstr = cables_infrastructure.uuid
   ,
	cables_app.django_content_type
where
	(django_content_type.app_label,
	django_content_type.model) = ('cables',
	'lineoperation')
;

insert
	into
	cables_app.cables_equipment (uuid,
	timestamp_create,
	timestamp_update,
	count,
	reference,
	comment,
	created_by_id,
	type_id,
	updated_by_id)
	--     (timestamp_create, timestamp_update, count, reference, comment, created_by_id, type_id, updated_by_id)
select
	uuid_generate_v4() as uuid,
	cables_operation.date as timestamp_create,
	cables_operation.date as timestamp_update,
	0 as count,
	null as reference,
	null as comment,
	1 as created_by_id,
	sinp_nomenclatures_nomenclature.id as type_id,
	1 as updated_by_id
from
	cables_app.cables_operation
join ${schema_name}.t_equipements_troncons_erdf on
	uuid_operation = cables_operation.uuid
join ${schema_name}.dico_type_equipement_troncon on
	t_equipements_troncons_erdf.id_type_equipement_troncon =
                                                             dico_type_equipement_troncon.id_type_equipement_troncon
join tmp.equipement_troncon on
	dico_type_equipement_troncon.id_type_equipement_troncon = equipement_troncon.id
join cables_app.sinp_nomenclatures_nomenclature
              on
	equipement_troncon.final_code = sinp_nomenclatures_nomenclature.code
	and type_id = 7;
--
INSERT INTO cables_app.cables_lineoperation (operation_ptr_id, geom)
select
	cables_operation.id,
	t_equipements_troncons_erdf.geom
from
	cables_app.cables_operation
join ${schema_name}.t_equipements_troncons_erdf on
	uuid_operation = cables_operation.uuid
;
-- INFO: MORTALITY DATA

with data as (
select
	t_especes.nom_espece,
	species_from_olddbs.cd_nom,
	coalesce(date,
	'1900-01-01') as date,
	t_cas_mortalite.geom,
	t_cas_mortalite.nb_cas,
	t_cas_mortalite.source,
	case
		when id_cause_mortalite = 1 then 'COD_EL'
		when id_cause_mortalite = 2 then 'COD_IM'
		else 'COD_UNKNOWN'
	end as death_cause
from
	${schema_name}.t_cas_mortalite
join ${schema_name}.t_especes on
	t_especes.id_espece = t_cas_mortalite.id_espece
join tmp.species_from_olddbs
                            on
	t_especes.nom_espece = species_from_olddbs.nom_espece
left join cables_app.species_species on
	code = cd_nom)
insert
	into
	cables_app.mortality_mortality(timestamp_create,
	timestamp_update,
	author,
	geom,
	date,
	count,
	created_by_id,
	data_source_id,
	death_cause_id,
	infrstr_id,
	species_id,
	updated_by_id)
select
	date,
	now(),
	1,
	st_transform(geom,
	4326),
	date,
	coalesce(nb_cas,
	1),
	1,
	null,
	nom_dc.id,
	null,
	species_species.id,
	1
from
	data
join cables_app.sinp_nomenclatures_nomenclature nom_dc on
	death_cause = nom_dc.code
join cables_app.species_species on
	data.cd_nom = species_species.code
order by
	date desc;


UPDATE cables_app.mortality_mortality
SET infrstr_id = cables_infrastructure.id
FROM cables_app.cables_infrastructure
         JOIN cables_app.cables_point ON cables_infrastructure.id = cables_point.infrastructure_ptr_id
WHERE st_within(st_transform(mortality_mortality.geom,2154), st_buffer(st_transform(cables_point.geom,2154),10));


commit;
