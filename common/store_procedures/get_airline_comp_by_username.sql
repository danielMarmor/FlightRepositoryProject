DROP FUNCTION IF EXISTS public.get_airline_comp_by_username(text);

CREATE OR REPLACE FUNCTION public.get_airline_comp_by_username(
	_username text)
    RETURNS TABLE(id bigint, name character varying, country_id integer, iata character varying, user_id bigint)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select ac.id as id,
			ac.name as name,
			ac.country_id as country_id,
			ac.iata as iata,
			ac.user_id as user_id
			from airine_companies ac
			join users usr on ac.user_id = usr.id
			where usr.username like _username;
		end;

$BODY$;

ALTER FUNCTION public.get_airline_comp_by_username(text)
    OWNER TO postgres;
