USE [WRI]
GO
-- Drop function if exists
--
IF object_id(N'STMove', N'FN') IS NOT NULL
    DROP FUNCTION [dbo].[STMove]
GO
-- Function: Move
--
CREATE FUNCTION dbo.STMove(@p_geometry  geometry,
                         @p_dX        FLOAT,
                         @p_dY        FLOAT,
                         @p_dZ        FLOAT,
                         @p_dM        FLOAT,
                         @p_round_x   INT = 3,
                         @p_round_y   INT = 3,
                         @p_round_z   INT = 2,
                         @p_round_m   INT = 2)
RETURNS geometry
BEGIN
  DECLARE
     @v_coord          INT = 0,
     @v_rows           INT = 0,
     @v_wkt            VARCHAR(MAX) = '',
     @v_token          VARCHAR(MAX),
     @v_delim          VARCHAR(MAX),
     @v_geometry       geometry,
     @v_x              FLOAT = 0.0,
     @v_y              FLOAT = 0.0,
     @v_z              FLOAT = NULL,
     @v_m              FLOAT = NULL;
  BEGIN
    IF ( @p_geometry IS NULL )
      RETURN NULL;
    IF ( @p_dX IS NULL AND @p_dY IS NULL AND @p_dZ IS NULL AND @p_dM IS NULL )
       RETURN CAST('One of deltas X,Y,Z and M must not be NULL.' AS VARCHAR(MAX)); -- geometry);
    SET @v_coord = 0;
    SET @v_rows  = 0;
    DECLARE Tokens CURSOR FAST_FORWARD FOR
      SELECT t.token, t.separator
        FROM dbo.Tokenizer(@p_geometry.AsTextZM(),' ,()') AS t;
    OPEN Tokens;
    FETCH NEXT FROM Tokens INTO @v_token, @v_delim;
    WHILE @@FETCH_STATUS = 0
    BEGIN
       IF ( @v_token IS NULL )  -- double delimiter
       BEGIN
          SET @v_wkt = @v_wkt + @v_delim
       END
       ELSE
       BEGIN
          IF ( @v_token NOT LIKE '[-0-9]%' )
          BEGIN
             SET @v_wkt = @v_wkt + @v_token + LTRIM(@v_delim)
          END
          ELSE -- @v_token LIKE '[0-9]%' )  
          BEGIN
             SET @v_coord = @v_coord + 1;
             IF ( @v_coord = 1 ) SET @v_x = CAST(@v_token AS FLOAT)
             IF ( @v_coord = 2 ) SET @v_y = CAST(@v_token AS FLOAT)
             IF ( @v_coord = 3 ) SET @v_z = CAST(@v_token AS FLOAT)
             IF ( @v_coord = 4 ) SET @v_m = CAST(@v_token AS FLOAT)
             IF ( @v_delim IN (',',')') )
             BEGIN
                SET @v_wkt = @v_wkt +
                   LTRIM(STR(round(@v_x + @p_dX, @p_round_x),24,@p_round_x)) + ' ' +
                   LTRIM(STR(round(@v_y + @p_dY, @p_round_y),24,@p_round_y)) +
                   CASE WHEN @v_z IS NULL THEN '' ELSE ' ' + LTRIM(STR(round(@v_z + @p_dZ, @p_round_z),24,@p_round_z)) END +
                   CASE WHEN @v_m IS NULL THEN '' ELSE ' ' + LTRIM(STR(round(@v_m + @p_dM, @p_round_m),24,@p_round_m)) END + @v_delim;
                SET @v_coord = 0;
             END;
           END;
       END;
       FETCH NEXT FROM Tokens INTO @v_token, @v_delim;
    END;
    CLOSE Tokens
    DEALLOCATE Tokens
    SET @v_geometry = geometry::STGeomFromText(@v_wkt,@p_geometry.STSrid);
    RETURN @v_geometry;
  END
END
GO