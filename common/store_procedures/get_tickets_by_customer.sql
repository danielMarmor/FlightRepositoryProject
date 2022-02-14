DROP FUNCTION IF EXISTS public.get_tickets_by_customer(bigint);
CREATE OR REPLACE FUNCTION public.get_tickets_by_customer(
	_customer_id bigint)
    RETURNS TABLE(id bigint, flight_id bigint, customer_id bigint)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select *
			from tickets tick
			where tick.customer_id =_customer_id;

		end;

$BODY$;

ALTER FUNCTION public.get_tickets_by_customer(bigint)
    OWNER TO postgres;