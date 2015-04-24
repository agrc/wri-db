delete from [WRI_Spatial].[dbo].[LINE] where StatusDescription != 'Complete' and project_fk in (
	select project_fk from [WRI_Spatial].[dbo].[LINE] where StatusDescription = 'Complete'
)

delete from [WRI_Spatial].[dbo].[POLY] where StatusDescription != 'Complete' and project_fk in (
	select project_fk from [WRI_Spatial].[dbo].[POLY] where StatusDescription = 'Complete'
)

delete from [WRI_Spatial].[dbo].[POINT] where StatusDescription != 'Complete' and project_fk in (
	select project_fk from [WRI_Spatial].[dbo].[POINT] where StatusDescription = 'Complete'
)