/****** Script for SelectTopNRows command from SSMS  ******/
SELECT * from [WRI_Spatial].[dbo].[LINE]
order by TypeDescription

select * from [WRI_Spatial].[dbo].[POINT]
order by TypeDescription

select * from [WRI_Spatial].[dbo].[POLY]
order by TypeDescription
