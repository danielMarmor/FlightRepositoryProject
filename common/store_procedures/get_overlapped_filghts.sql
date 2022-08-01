-- FUNCTION: public.get_overlapped_filghts(bigint, bigint)

DROP FUNCTION IF EXISTS public.get_overlapped_filghts(bigint, bigint);

CREATE OR REPLACE FUNCTION public.get_overlapped_filghts(
	_customer_id bigint,
	_new_flight_id bigint)
    RETURNS TABLE(id bigint, airline_company_id bigint, origin_country_id integer, destination_country_id integer, departure_time timestamp without time zone, landing_time timestamp without time zone,  remaining_tickets integer, price numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
		return QUERY
		with new_fli as (
			select * from flights fli
			where fli.id = _new_flight_id
			limit 1
		)
		select fli.*
		from tickets tick
		join flights fli on tick.flight_id =fli.id
		where tick.customer_id =_customer_id
		and fli.id <>(select f.id from new_fli f limit 1 )
		and not(
			(fli.departure_time > (select f.landing_time from new_fli f limit 1)
			and fli.landing_time > (select f.landing_time from new_fli f limit 1))
			or
			(fli.departure_time  < (select f.departure_time from new_fli f limit 1)
			and fli.landing_time < (select f.departure_time from new_fli f limit 1))
		);
		end;

$BODY$;

ALTER FUNCTION public.get_overlapped_filghts(bigint, bigint)
    OWNER TO postgres;
