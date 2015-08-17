insert into dbo.[POINT] (GUID,Project_FK,Project_ID,Shape,StatusDescription)
values ('00000000-0000-0000-0000-000000000001',
        '00000000-0000-0000-0000-000000000001',
        -1,
        geometry::STGeomFromText('MULTIPOINT ((40.76726 -111.86176))', 3857),
        'temporary')

insert into dbo.[LINE] (GUID,Project_FK,Project_ID,Shape,StatusDescription)
values ('00000000-0000-0000-0000-000000000001',
        '00000000-0000-0000-0000-000000000001',
        -1,
         geometry::STGeomFromText('LINESTRING (40.76726 -111.86176, 41.76726 -110.86176)', 3857),
        'temporary')

insert into dbo.[POLY] (GUID,Project_FK,Project_ID,Shape,StatusDescription)
values ('00000000-0000-0000-0000-000000000001',
        '00000000-0000-0000-0000-000000000001',
        -1,
        geometry::STGeomFromText('POLYGON ((40.76726 -111.86176, 41.76726 -111.86176, 43.76726 -109.86176, 40.76726 -111.86176))', 3857),
        'temporary')
