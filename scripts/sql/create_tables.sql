DROP TABLE [Wri_Spatial].[dbo].POLY

CREATE TABLE [Wri_Spatial].[dbo].POLY(
	[FeatureID] [int] IDENTITY(1,1) NOT NULL,
    Type nvarchar(255) NULL,
	GUID uniqueidentifier NOT NULL,
	Project_FK uniqueidentifier NOT NULL,
    Project_ID bigint NOT NULL,  
	Completed int NULL,
	Status varchar(50) NULL,
	Shape geometry NULL,
	PRIMARY KEY CLUSTERED 
(
	[FeatureID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

DROP TABLE [Wri_Spatial].[dbo].POINT

CREATE TABLE [Wri_Spatial].[dbo].POINT(
	FeatureID int IDENTITY(1,1) NOT NULL,
	Type nvarchar(50) NULL,
	SubType nvarchar(50) NULL,
	Action nvarchar(255) NULL,
	Description nvarchar(255) NULL,
	GUID uniqueidentifier NOT NULL,
	Project_FK uniqueidentifier NOT NULL,
    Project_ID bigint NOT NULL,
	Completed int NULL,
	Status varchar(50) NULL,
	Shape geometry  NULL,
	PRIMARY KEY CLUSTERED 
(
	[FeatureID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

DROP TABLE [Wri_Spatial].[dbo].LINE

CREATE TABLE [Wri_Spatial].[dbo].LINE(
	FeatureID int IDENTITY(1,1) NOT NULL,
	Type nvarchar(255) NULL,
	SubType nvarchar(50) NULL,
	Action nvarchar(255) NULL,
	GUID uniqueidentifier NOT NULL,
	Project_FK uniqueidentifier NOT NULL,
    Project_ID bigint NOT NULL,
	Completed int NULL,
	Status varchar(50) NULL,
	Shape geometry NULL,
	PRIMARY KEY CLUSTERED 
(
	[FeatureID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]