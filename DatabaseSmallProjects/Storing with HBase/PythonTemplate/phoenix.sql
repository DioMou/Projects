--drop VIEW "powers";
CREATE VIEW "powers" (pk VARCHAR PRIMARY KEY, "personal"."hero" VARCHAR,"personal"."power" VARCHAR,"professional"."name" VARCHAR,"professional"."xp" VARCHAR,"custom"."color" VARCHAR);


select p."professional"."name" "Name1",p1."professional"."name" "Name2",p1."personal"."power" "Power" from "powers" as p inner join "powers" as p1 ON p."personal"."power"=p1."personal"."power" WHERE p."personal"."power" =p1."personal"."power" and p."professional"."name"<>'normalman' and p1."professional"."name"<>'normalman' AND p."personal"."hero"='yes' AND p1."personal"."hero"='yes';
