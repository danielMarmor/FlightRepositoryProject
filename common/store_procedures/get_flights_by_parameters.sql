-- FUNCTION: public.get_flights_by_parameters(integer, integer, timestamp without time zone, timestamp without time zone)

DROP FUNCTION IF EXISTS public.get_flights_by_parameters(integer, integer, timestamp without time zone, timestamp without time zone);

CREATE OR REPLACE FUNCTION public.get_flights_by_parameters(
	_origin_counry_id integer,
	_detination_country_id integer,
	_start_date timestamp without time zone,
	_end_date timestamp without time zone)
    RETURNS TABLE(flight_id bigint,
				  airline_company_id bigint,
				  airline_company_name character varying,
				  airline_company_img_url character varying,
				  origin_country_id integer,
				  origin_country_name character varying,
				  origin_country_airport_abbr character varying,
				  destination_country_id integer,
				  dest_country_name character varying,
				  dest_country_airport_abbr character varying,
				  departure_time timestamp without time zone,
				  landing_time timestamp without time zone,
				  price numeric(18, 2),
				  remaining_tickets integer)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		declare NO_COUNTRY bigint := -1;
		declare MIN_DATE date := to_date('01/01/0001', 'DD/MM/YYYY');
		declare MAX_DATE date := to_date('31/12/9999', 'DD/MM/YYYY');

		begin
			return QUERY
			select
			fli.id flight_id,
			fli.airline_company_id airline_company_id,
			ac.name airline_company_name,
			ac.image_url airline_company_img_url,
			fli.origin_country_id origin_country_id,
			co_orig.name origin_country_name,
			co_orig.airport_abbr origin_country_airport_abbr,
			fli.destination_country_id destination_country_id,
			co_dest.name dest_country_name,
			co_dest.airport_abbr dest_country_airport_abbr,
			fli.departure_time departure_time,
			fli.landing_time landing_time,
			fli.price price,
			fli.remaining_tickets remaining_tickets
			from
			flights fli
			join airine_companies ac on fli.airline_company_id =ac.id
			join countries co_orig on fli.origin_country_id = co_orig.id
			join countries co_dest on fli.destination_country_id = co_dest.id
			where
			(_origin_counry_id is null or fli.origin_country_id =_origin_counry_id)
			and (_detination_country_id is null or fli.destination_country_id =_detination_country_id)
			and ((_start_date is null and fli.departure_time >= MIN_DATE)
			or fli.departure_time >= _start_date)
			and ((_end_date is null and fli.landing_time <= MAX_DATE)
			or fli.landing_time <=_end_date);
		end;

$BODY$;

ALTER FUNCTION public.get_flights_by_parameters(integer, integer, timestamp without time zone, timestamp without time zone)
    OWNER TO postgres;
