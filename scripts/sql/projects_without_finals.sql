select '''' +convert(nvarchar(50), Project_FK) + '''' from WRIADMIN where status = 3 and
    0 = (
        select sum (featureCount) as featureCount from (
            select count(guid) as featureCount from WRIFINALAFFECTEDAREA where CompletedProject_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIFINALDAM where CompletedProject_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIFINALFENCE where CompletedProject_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIFINALGUZZLER where CompletedProject_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIFINALPIPELINE where CompletedProject_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIFINALPOINTS where CompletedProject_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIFINALTREATMENTAREA where CompletedProject_FK = wriadmin.project_fk
        ) as final_features) and
    1 <= (
        select sum(featureCount) as featureCount from (
            select count(guid) as featureCount from WRIAFFECTEDAREA where Project_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIDAM where Project_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIFENCE where Project_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIGUZZLER where Project_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIPIPELINE where Project_FK = wriadmin.project_fk
                union all
            select count(guid) from WRIPOINTS where Project_FK = wriadmin.project_fk
                union all
            select count(guid) from WRITREATMENTAREA where Project_FK = wriadmin.project_fk
        ) as project_features)