-- FUNCTION: public.get_sales_by_airlines(text, text, bigint)

DROP FUNCTION IF EXISTS public.get_sales_by_airlines(text, text, bigint);

CREATE OR REPLACE FUNCTION public.get_sales_by_airlines(
	_start_date text,
	_end_date text,
	_destination_country_id bigint)
    RETURNS TABLE(airline_id bigint, airline_name character varying, count_tickets bigint, sum_sales numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
		    return QUERY
			select * from
			(select
			air.id airline_id,
			air.name airline_name,
			count(tick.id) count_tickets,
			sum(tick.price) sum_sales
			from
			flights fli
			join tickets tick on fli.id = tick.flight_id
			join airine_companies air on fli.airline_company_id = air.id
			where fli.departure_time >= to_date(_start_date, 'DD/MM/YYYY') and
			fli.departure_time < to_date(_end_date, 'DD/MM/YYYY') and
			(fli.destination_country_id = _destination_country_id or _destination_country_id = -1)
			group by
			air.id,
			air.name) airlines
			order by airlines.sum_sales desc
			limit 20;
		end;

$BODY$;

ALTER FUNCTION public.get_sales_by_airlines(text, text, bigint)
    OWNER TO postgres;
