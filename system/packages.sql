select *
  from (select count(*) cnt, h.owner, h.object_name, min(h.ddl_date), max(h.ddl_date)
          from tehno.ddl_history_2 h
         where h.ddl_date between to_date('01.06.2019', 'dd.mm.yyyy') and
               SYSDATE
           and h.object_type like 'PACKAGE BODY'
         group by object_name, owner)
 order by cnt desc
