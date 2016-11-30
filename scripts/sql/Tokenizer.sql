USE [WRI]
GO
-- Drop function if exists
--
IF EXISTS (SELECT *
             FROM dbo.sysobjects
            WHERE id = object_id (N'[dbo].[Tokenizer]')
              AND OBJECTPROPERTY(id, N'IsTableFunction') = 1)
DROP FUNCTION [dbo].[Tokenizer]
GO
--
-- Now let's create it
--
/*********************************************************************************
** @function    : Tokenizer
** @precis      : Splits any string into its tokens.
** @description : Supplied a string and a list of separators this function
**                returns resultant tokens as a table collection.
** @example     : SELECT t.token
**                  FROM dbo.tokenizer('The rain in spain, stays mainly on the plain.!',' ,.!') t;
** @param       : p_string. The string to be Tokenized.
** @param       : p_separators. The characters that are used to split the string.
** @history     : Pawel Barut, http://pbarut.blogspot.com/2007/03/yet-another-tokenizer-in-oracle.html
** @history     : Simon Greener - Jul 2006 - Original coding (extended SQL)
** @history     : Simon Greener - Aug 2008 - Converted to SQL Server 2008
** @history     : Simon Greener - Aug 2012 - Converted to SQL Server 2012 and return separators
**/
CREATE FUNCTION [dbo].[Tokenizer](@p_string     VARCHAR(MAX),
                                  @p_separators VARCHAR(254))
  RETURNS @varchar_table TABLE
 (
   id        INT,
   token     VARCHAR(MAX),
   separator VARCHAR(MAX)
  )
AS
BEGIN
  BEGIN
    WITH MyCTE AS (
      SELECT c.beg, c.sep, ROW_NUMBER() OVER(ORDER BY c.beg ASC) AS rid
        FROM (SELECT b.beg, c.sep
                FROM (SELECT a.beg
                        FROM (SELECT c.IntValue AS beg
                                FROM dbo.generate_series(1,DATALENGTH(@p_string),1) c
                              ) a
                      ) b,
                      (SELECT SUBSTRING(@p_separators,d.IntValue,1) AS sep
                          FROM dbo.generate_series(1,DATALENGTH(@p_separators),1) d
                        ) c
                WHERE CHARINDEX(c.sep,SUBSTRING(@p_string,b.beg,1)) > 0
              UNION ALL SELECT 0 AS beg, CAST(NULL AS VARCHAR) AS sep
             ) c
    )
    INSERT INTO @varchar_table
    SELECT ROW_NUMBER() OVER (ORDER BY a.rid ASC) AS Id,
           CASE WHEN DataLength(a.token) = 0 THEN NULL ELSE a.token END AS token,
           a.sep
      FROM (SELECT d.rid,
                   SUBSTRING(@p_string, (d.beg + 1), (Lead(d.beg,1) OVER (ORDER BY d.rid ASC) - d.beg - 1) ) AS token,
                   Lead(d.sep,1) OVER (ORDER BY d.rid ASC) AS sep
              FROM MyCTE d
           ) AS a
     WHERE DataLength(a.token) <> 0 OR DataLength(a.sep) <> 0;
    RETURN;
  END;
END
GO
