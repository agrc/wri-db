truncate table [dbo].[POINT]

truncate table [dbo].[LINE]

truncate table [dbo].[POLY]

truncate table [dbo].[STREAM]

truncate table [dbo].[FOCUSAREA]

truncate table [dbo].[LANDOWNER]

truncate table [dbo].[SGMA]

truncate table [dbo].[COUNTY]

update [dbo].[Project] set Centroid = NULL
