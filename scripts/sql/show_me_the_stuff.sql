/****** Script for SelectTopNRows command from SSMS  ******/
SELECT * from [WRI_Spatial].[dbo].[LINE]
order by TypeDescription

select * from wri_spatial.dbo.point
order by TypeDescription

select * from wri_spatial.dbo.poly
order by TypeDescription
