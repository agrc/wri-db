delete from [dbo].[LINE] where StatusDescription != 'Completed' and project_fk in (
	select project_fk from [dbo].[LINE] where StatusDescription = 'Completed'
)

delete from [dbo].[POLY] where StatusDescription != 'Completed' and project_fk in (
	select project_fk from [dbo].[POLY] where StatusDescription = 'Completed'
)

delete from [dbo].[POINT] where StatusDescription != 'Completed' and project_fk in (
	select project_fk from [dbo].[POINT] where StatusDescription = 'Completed'
)
