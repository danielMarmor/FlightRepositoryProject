-- FUNCTION: public.get_administrator_by_username(text)

DROP FUNCTION IF EXISTS public.get_administrator_by_username(text);

CREATE OR REPLACE FUNCTION public.get_administrator_by_username(
	_username text)
    RETURNS TABLE(id integer,
				  first_name character varying,
				  last_name character varying, 
				  user_id bigint,
				  image_url character varying) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select ad.*
			from administrators ad
			join users usr on ad.user_id = usr.id
			where usr.username like _username;
		end;

$BODY$;

ALTER FUNCTION public.get_administrator_by_username(text)
    OWNER TO postgres;
