DROP FUNCTION IF EXISTS public.get_flights_by_customer(bigint);
CREATE OR REPLACE FUNCTION public.get_flights_by_customer(
	_customer_id bigint)
    RETURNS TABLE(flight_id bigint, airline_company_id bigint, airline_company_name character varying, origin_country_id integer, origin_country_name character varying, destination_country_id integer, dest_country_name character varying, departure_time timestamp without time zone, landing_time timestamp without time zone, remaining_tickets integer)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
			return QUERY
			select * from flights fli
			join tickets tick on fli.id = tick.flight_id
			where tick.customer_id= _customer_id;
		end;

$BODY$;

ALTER FUNCTION public.get_flights_by_customer(bigint)
    OWNER TO postgres;
