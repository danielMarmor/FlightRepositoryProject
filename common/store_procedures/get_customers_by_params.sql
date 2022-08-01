-- FUNCTION: public.get_customers_by_params(character varying)

DROP FUNCTION IF EXISTS public.get_customers_by_params(character varying);

CREATE OR REPLACE FUNCTION public.get_customers_by_params(
	_search character varying)
    RETURNS TABLE(id bigint, first_name character varying, last_name character varying, address character varying, phone_number character varying, credit_card_number character varying, user_id bigint, image_url character varying)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select
			*
			from customers cust
			where
			_search is null
			or
			((cust.first_name || ' ' || cust.last_name) like ('%' || _search || '%')
		     or (cust.last_name || ' ' || cust.first_name) like ('%' || _search || '%'));

		end;

$BODY$;

ALTER FUNCTION public.get_customers_by_params(character varying)
    OWNER TO postgres;
