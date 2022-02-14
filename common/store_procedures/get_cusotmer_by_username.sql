DROP FUNCTION IF EXISTS public.get_cusotmer_by_username(text);
CREATE OR REPLACE FUNCTION public.get_cusotmer_by_username(
	_username text)
    RETURNS TABLE(id bigint, first_name character varying, last_name character varying, address character varying, phone_number character varying, credit_card_number character varying, user_id bigint)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select cust.* from customers cust
			join users usr on cust.user_id = usr.id
			where usr.username like _username;
		end;

$BODY$;

ALTER FUNCTION public.get_cusotmer_by_username(text)
    OWNER TO postgres;