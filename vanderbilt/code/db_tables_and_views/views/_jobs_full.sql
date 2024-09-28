-- public."_jobs_full" source

CREATE OR REPLACE VIEW public."_jobs_full"
AS WITH benefits_grouped AS (
         SELECT DISTINCT jb.job_x_id,
            string_agg(jb.job_benefit_value::text, ', '::text) AS rel_benefit_values,
            string_agg(DISTINCT jb.benefit_cluster::text, ', '::text) AS rel_benefit_clusters
           FROM _job_benefits jb
          GROUP BY jb.job_x_id
        ), requirements_grouped AS (
         SELECT DISTINCT jr.job_x_id,
            string_agg(jr.job_requirement_name::text, ', '::text) AS rel_requirement_names,
            string_agg(DISTINCT jr.requirement_cluster::text, ', '::text) AS rel_requirement_clusters
           FROM _job_requirements jr
          GROUP BY jr.job_x_id
        )
 SELECT ja.job_x_id,
    ja.display_title,
    ja.job_description,
    ja.job_type,
    ja.snippet,
    ja.sponsored,
    ja.shift_type,
    ja.extracted_salary_min,
    ja.extracted_salary_type,
    ja.salary_snippet_currency,
    ja.company_x_id,
    ja.job_location,
    ja.min_hour_salary,
    ja.job_function_cluster,
    bg.rel_benefit_values,
    bg.rel_benefit_clusters,
    rg.rel_requirement_names,
    rg.rel_requirement_clusters,
    c.company AS company_name,
    c.company_rating,
    c.industry_cluster_1,
    c.industry_cluster_2,
    c.company_review_count
   FROM _job_attributes ja
     LEFT JOIN benefits_grouped bg ON bg.job_x_id = ja.job_x_id
     LEFT JOIN requirements_grouped rg ON rg.job_x_id = ja.job_x_id
     LEFT JOIN _companies c ON c.company_x_id = ja.company_x_id;
