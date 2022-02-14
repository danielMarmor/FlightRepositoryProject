DROP FUNCTION IF EXISTS public.get_arrival_flights(integer);
CREATE OR REPLACE FUNCTION public.get_arrival_flights(
	_country_id integer)
    RETURNS TABLE(flight_id bigint, airline_company_id bigint, airline_company_name character varying, origin_country_id integer, origin_country_name character varying, destination_country_id integer, dest_country_name character varying, departure_time timestamp without time zone, landing_time timestamp without time zone, remaining_tickets integer)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$

        declare start_date timestamp without time zone:= current_date;
		--declare start_date timestamp without time zone:= make_date(2022, 01, 20);
		declare end_date timestamp without time zone:=start_date + INTERVAL '12 HOUR';
		begin
			return QUERY
			select
			fli.id flight_id,
			fli.airline_company_id airline_company_id,
			ac.name airline_company_name,
			fli.origin_country_id origin_country_id,
			co_orig.name origin_country_name,
			fli.destination_country_id destination_country_id,
			co_dest.name dest_country_name,
			fli.departure_time departure_time,
			fli.landing_time landing_time,
			fli.remaining_tickets remaining_tickets
			from
			flights fli
			join airine_companies ac on fli.airline_company_id =ac.id
			join countries co_orig on fli.origin_country_id = co_orig.id
			join countries co_dest on fli.destination_country_id = co_dest.id
			where
			fli.destination_country_id = _country_id
			and fli.landing_time >=start_date
			and fli.landing_time  < end_date;
		end;

$BODY$;

ALTER FUNCTION public.get_arrival_flights(integer)
    OWNER TO postgres;