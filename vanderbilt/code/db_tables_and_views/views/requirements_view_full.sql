-- public.requirements_view_full source

CREATE OR REPLACE VIEW public.requirements_view_full
AS SELECT jr.job_x_id,
    ja.min_hour_salary,
    ja.job_function_cluster,
    jr.job_requirement_name,
    jr.requirement_cluster,
    c.company,
    c.company_rating,
    c.industry_cluster_1,
    c.industry_cluster_2,
    c.company_review_count
   FROM _job_attributes ja
     RIGHT JOIN _job_requirements jr ON ja.job_x_id = jr.job_x_id
     LEFT JOIN _companies c ON c.company_x_id = ja.company_x_id;
