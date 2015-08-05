DROP TABLE [dbo].POLY

CREATE TABLE [dbo].[POLY](
	[FeatureID] [bigint] IDENTITY(1,1) NOT NULL,
	[TypeDescription] [nvarchar](255) NULL,
	[TypeCode] [int] NULL,
	[GUID] [uniqueidentifier] NOT NULL,
	[Project_FK] [uniqueidentifier] NOT NULL,
	[Project_ID] [bigint] NOT NULL,
	[StatusDescription] [varchar](50) NULL,
	[StatusCode] [int] NULL,
	[Shape] [geometry] NULL,
	[AreaAcres] [numeric](38, 8) NULL,
 CONSTRAINT [PK__POLY__82230A2972370709] PRIMARY KEY CLUSTERED
(
	[FeatureID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

DROP TABLE [dbo].POINT

CREATE TABLE [dbo].[POINT](
	[FeatureID] [bigint] IDENTITY(1,1) NOT NULL,
	[TypeDescription] [nvarchar](255) NULL,
	[TypeCode] [int] NULL,
	[FeatureSubTypeID] [int] NULL,
	[FeatureSubTypeDescription] [nvarchar](255) NULL,
	[ActionID] [int] NULL,
	[ActionDescription] [nvarchar](255) NULL,
	[Description] [nvarchar](255) NULL,
	[GUID] [uniqueidentifier] NOT NULL,
	[Project_FK] [uniqueidentifier] NOT NULL,
	[Project_ID] [bigint] NOT NULL,
	[StatusDescription] [varchar](50) NULL,
	[StatusCode] [int] NULL,
	[Shape] [geometry] NULL,
 CONSTRAINT [PK__POINT__82230A299395AD24] PRIMARY KEY CLUSTERED
(
	[FeatureID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

DROP TABLE [dbo].LINE

CREATE TABLE [dbo].[LINE](
	[FeatureID] [bigint] IDENTITY(1,1) NOT NULL,
	[TypeDescription] [nvarchar](255) NULL,
	[TypeCode] [int] NULL,
	[FeatureSubTypeID] [int] NULL,
	[FeatureSubTypeDescription] [nvarchar](255) NULL,
	[ActionID] [int] NULL,
	[ActionDescription] [nvarchar](255) NULL,
	[Description] [nvarchar](255) NULL,
	[GUID] [uniqueidentifier] NOT NULL,
	[Project_FK] [uniqueidentifier] NOT NULL,
	[Project_ID] [bigint] NOT NULL,
	[StatusDescription] [varchar](50) NULL,
	[StatusCode] [int] NULL,
	[Shape] [geometry] NULL,
	[LengthFeet] [numeric](12, 2) NULL,
 CONSTRAINT [PK__LINE__82230A29116B9894] PRIMARY KEY CLUSTERED
(
	[FeatureID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
