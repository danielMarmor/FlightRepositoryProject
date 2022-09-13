-- FUNCTION: public.get_count_flights(text, text)

DROP FUNCTION IF EXISTS public.get_count_flights(text, text);

CREATE OR REPLACE FUNCTION public.get_count_flights(
	_start_date text,
	_end_date text)
    RETURNS TABLE(country_id integer, country_name character varying, count_flights bigint)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
		    return QUERY
			select * from
			(select
			cou.id country_id,
			cou.name country_name,
			count(fli.id) count_flights
			from
			flights fli
			join countries cou on fli.destination_country_id = cou.id
			where fli.departure_time >= to_date(_start_date, 'DD/MM/YYYY') and
			fli.departure_time < to_date(_end_date, 'DD/MM/YYYY')
			group by
			cou.id,
			cou.name) countries
			order by countries.count_flights desc
			limit 10;
		end;

$BODY$;

ALTER FUNCTION public.get_count_flights(text, text)
    OWNER TO postgres;
