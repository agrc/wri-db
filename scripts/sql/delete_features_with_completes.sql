delete from [WRI].[dbo].[LINE] where StatusDescription != 'Complete' and project_fk in (
	select project_fk from [WRI].[dbo].[LINE] where StatusDescription = 'Complete'
)

delete from [WRI].[dbo].[POLY] where StatusDescription != 'Complete' and project_fk in (
	select project_fk from [WRI].[dbo].[POLY] where StatusDescription = 'Complete'
)

delete from [WRI].[dbo].[POINT] where StatusDescription != 'Complete' and project_fk in (
	select project_fk from [WRI].[dbo].[POINT] where StatusDescription = 'Complete'
)
