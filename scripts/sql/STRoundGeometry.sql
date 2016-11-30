USE [WRI]
GO
-- Drop if exists
--
IF object_id(N'STRoundGeometry', N'FN') IS NOT NULL
    DROP FUNCTION dbo.STRoundGeometry
GO
-- Now create
--
CREATE FUNCTION dbo.STRoundGeometry(@p_geometry geometry,
                                    @p_round_x   INT = 3,
                                    @p_round_y   INT = 3,
                                    @p_round_z   INT = 2,
                                    @p_round_m   INT = 2)
RETURNS geometry
AS
BEGIN
  DECLARE
    @v_geom geometry;
  BEGIN
    IF ( @p_geometry IS NULL )
      RETURN @p_geometry;
    SET @v_geom = dbo.STMove(@p_geometry,0.0,0.0,0.0,0.0,@p_round_x,@p_round_y,@p_round_z,@p_round_m);
  END;
  RETURN @v_geom;
END;
GO