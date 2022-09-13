-- FUNCTION: public.get_administrators_by_params(character varying)

DROP FUNCTION IF EXISTS public.get_administrators_by_params(character varying);

CREATE OR REPLACE FUNCTION public.get_administrators_by_params(
	_search character varying)
    RETURNS TABLE(id integer,
				  first_name character varying,
				  last_name character varying,
				  email character varying,
				  image_url character varying
				 )
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$

		begin
		    return QUERY
			select
			adm.id,
			adm.first_name,
			adm.last_name,
			usr.email,
			adm.image_url
			from administrators adm
			join users usr on adm.user_id = usr.id
			where
			(_search is null
			or
			((adm.first_name || ' ' || adm.last_name) like ('%' || _search || '%')
		     or (adm.last_name || ' ' || adm.first_name) like ('%' || _search || '%')))
			limit 50;
		end;

$BODY$;

ALTER FUNCTION public.get_administrators_by_params(character varying)
    OWNER TO postgres;
