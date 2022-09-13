-- FUNCTION: public.get_flights_by_airline_id(bigint)

DROP FUNCTION IF EXISTS public.get_flights_by_airline_id(bigint);

CREATE OR REPLACE FUNCTION public.get_flights_by_airline_id(
	_airline_id bigint)
    RETURNS TABLE(flight_id bigint,
				  airline_company_id bigint,
				  airline_company_name character varying,
				  airline_iata character varying,
				  origin_country_id integer,
				  origin_country_name character varying,
				  origin_country_airport_abbr character varying,
				  destination_country_id integer,
				  dest_country_name character varying,
				  dest_country_airport_abbr character varying,
				  departure_time text, landing_time text,
				  price numeric, num_seats bigint,
				  distance numeric,
				  remaining_tickets integer,
				  revenues numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$

		begin
			return QUERY
			select
			fli.id flight_id,
			fli.airline_company_id airline_company_id,
			ac.name airline_company_name,
			ac.iata airline_iata,
			fli.origin_country_id origin_country_id,
			co_orig.name origin_country_name,
			co_orig.airport_abbr  origin_country_airport_abbr,
			fli.destination_country_id destination_country_id,
			co_dest.name dest_country_name,
			co_dest.airport_abbr  dest_country_airport_abbr,
			TO_CHAR(fli.departure_time, 'DD/MM/YYYY HH24:MI:SS') departure_time,
			TO_CHAR(fli.landing_time, 'DD/MM/YYYY HH24:MI:SS') landing_time,
			fli.price price,
			fli.num_seats num_seats,
			fli.distance distance,
			fli.remaining_tickets remaining_tickets,
			(select sum(tick.price) from tickets tick where tick.flight_id =fli.id) revenues
			from
			flights fli
			join airine_companies ac on fli.airline_company_id =ac.id
			join countries co_orig on fli.origin_country_id = co_orig.id
			join countries co_dest on fli.destination_country_id = co_dest.id
			where
			fli.airline_company_id =_airline_id;
		end;

$BODY$;

ALTER FUNCTION public.get_flights_by_airline_id(bigint)
    OWNER TO postgres;
