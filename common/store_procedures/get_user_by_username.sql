DROP FUNCTION IF EXISTS public.get_user_by_username(text);
CREATE OR REPLACE FUNCTION public.get_user_by_username(
	_username text)
    RETURNS TABLE(id bigint, username character varying, password character varying, email character varying, user_role integer)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select * from users usr
			where usr.username like _username;
		end;

$BODY$;

ALTER FUNCTION public.get_user_by_username(text)
    OWNER TO postgres;
