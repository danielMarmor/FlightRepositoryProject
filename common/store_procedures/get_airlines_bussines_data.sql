-- FUNCTION: public.get_airlines_bussines_data(character varying)

-- DROP FUNCTION IF EXISTS public.get_airlines_bussines_data(character varying);

CREATE OR REPLACE FUNCTION public.get_airlines_bussines_data(
	_search character varying)
    RETURNS TABLE(id bigint, country_id integer, name character varying, email character varying, iata character varying, last_activity_date timestamp without time zone, num_flights bigint, sum_sales numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		declare EMPTY_DATE timestamp without time zone:=TO_DATE('01/01/0001', 'DD/MM/YYYY');
		begin
		    return QUERY
			select
			data_flights.airline_id id,
			data_flights.country_id country_id,
		 	data_flights.airline_name name,
			data_flights.airline_email email,
			data_flights.airline_iata iata,
			max(data_flights.flight_date) last_activity_date,
			sum(case when data_flights.flight_id = 0 then 0 else 1 end) num_flights,
			sum(data_flights.num_tickets * data_flights.flight_price) sum_sales
			from
			(select
			airline.id airline_id,
			airline.country_id country_id,
		 	airline.name airline_name,
			airline.iata airline_iata,
		 	usr.email airline_email,
			coalesce(fli.id, 0) flight_id,
			coalesce(fli.price, 0) flight_price,
			coalesce(fli.departure_time, TO_DATE('01/01/0001', 'DD/MM/YYYY')) flight_date,
			count(coalesce(tick.id, 0)) num_tickets
			from airine_companies airline
			join users usr on airline.user_id = usr.id
			left join flights fli on airline.id = fli.airline_company_id
			left join tickets tick on coalesce(fli.id, 0) = tick.flight_id
			where
			(_search is null or lower(airline.name) like ('%' || lower(_search) || '%'))
		 	group by
		 	airline.id,
			airline.country_id,
		 	airline.name,
			airline.iata,
			usr.email,
			coalesce(fli.id, 0),
			coalesce(fli.price, 0),
			coalesce(fli.departure_time, TO_DATE('01/01/0001', 'DD/MM/YYYY'))) data_flights
			group by
			data_flights.airline_id,
			data_flights.country_id,
		 	data_flights.airline_name,
			data_flights.airline_email,
			data_flights.airline_iata;
		end;

$BODY$;

ALTER FUNCTION public.get_airlines_bussines_data(character varying)
    OWNER TO postgres;
