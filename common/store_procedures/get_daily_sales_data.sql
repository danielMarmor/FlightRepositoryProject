-- FUNCTION: public.get_daily_sales_data(text, text, bigint)

DROP FUNCTION IF EXISTS public.get_daily_sales_data(text, text, bigint);

CREATE OR REPLACE FUNCTION public.get_daily_sales_data(
	_start_date text,
	_end_date text,
	_destination_country_id bigint)
    RETURNS TABLE(result_date date, sum_sales numeric)
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
		begin
		    return QUERY
			select
			days.day result_date,
			sum(coalesce(tick.price, 0)) result_sales
			from
			(SELECT t.day::date
			FROM  generate_series(_start_date::timestamp
			,_end_date::timestamp
			,interval  '1 day') AS t(day)) days
			left join flights fli on
			fli.departure_time >= days.day and
			fli.departure_time < (days.day + INTERVAL '1 day') and
			fli.destination_country_id = (case when _destination_country_id = -1 then fli.destination_country_id else _destination_country_id end)
			left join tickets tick on coalesce(fli.id, 0) = tick.flight_id
			group by
			days.day
			order by days.day asc;
		end;

$BODY$;

ALTER FUNCTION public.get_daily_sales_data(text, text, bigint)
    OWNER TO postgres;
