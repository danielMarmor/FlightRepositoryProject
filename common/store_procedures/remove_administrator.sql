DROP PROCEDURE IF EXISTS public.remove_administrator(bigint);

CREATE OR REPLACE PROCEDURE public.remove_administrator(
	IN _administrator_id bigint)
LANGUAGE 'plpgsql'
AS $BODY$
	declare administrator_user_id bigint;
	begin
		select ad.user_id into administrator_user_id
		from administrators ad
		where ad.id =_administrator_id;
		delete from administrators ad
		where ad.id = _administrator_id;
		--USER
		delete from users usr
		where usr.id = administrator_user_id;
	end;
$BODY$;
