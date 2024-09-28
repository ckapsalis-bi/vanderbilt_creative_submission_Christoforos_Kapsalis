alter table _job_attributes
add column job_function_cluster varchar(255);

UPDATE _job_attributes
SET job_function_cluster = 
    CASE 
        WHEN lower(display_title) LIKE '%customer ser%' OR lower(display_title) LIKE '%customer care%' OR lower(display_title) LIKE '%customer exper%' 
            OR lower(display_title) LIKE '%client ser%' OR lower(display_title) LIKE '%call%' OR lower(display_title) LIKE '%dispatcher%' THEN 'Customer Service & Support'
        
        WHEN lower(display_title) LIKE '%content%' OR lower(display_title) LIKE '%copywriter%' OR lower(display_title) LIKE '%graphic designer%'
            OR lower(display_title) LIKE '%videographer%' OR lower(display_title) LIKE '%photographer%' THEN 'Creative & Scientific'
        
        WHEN lower(display_title) LIKE '%sales%' OR lower(display_title) LIKE '%account%' OR lower(display_title) LIKE '%marketing%' OR lower(display_title) LIKE '%business analyst%'
            OR lower(display_title) LIKE '%engagement specialist%' OR lower(display_title) LIKE '%inbound%' OR lower(display_title) LIKE '%intellig%' OR lower(display_title) LIKE '%brand%' THEN 'Sales & Marketing'

        WHEN lower(display_title) LIKE '%nurse%' OR lower(display_title) LIKE '%optometrist%' OR lower(display_title) LIKE '%physical%' 
            OR lower(display_title) LIKE '%lab tech%' OR lower(display_title) LIKE '%caregiver%' OR lower(display_title) LIKE '%behavior an%'
            OR lower(display_title) LIKE '%patient%' OR lower(display_title) LIKE '%bioinformatics%' OR lower(display_title) LIKE '%clinical%'
            OR lower(display_title) LIKE '%trauma%' OR lower(display_title) LIKE '%veterin%' OR lower(display_title) LIKE '%clinical%'
            OR lower(display_title) LIKE '%medic%' OR lower(display_title) LIKE '%dental%' OR lower(display_title) LIKE '%injury%' 
            OR lower(display_title) LIKE '%emergency%' OR lower(display_title) LIKE '%health%' OR lower(display_title) LIKE '%pharma%' THEN 'Healthcare & Medical'
        
        WHEN lower(display_title) LIKE '%warehouse%' OR lower(display_title) LIKE '%forklift%' OR lower(display_title) LIKE '%freight%'
            OR lower(display_title) LIKE '%transportation%' OR lower(display_title) LIKE '%shipping%' OR lower(display_title) LIKE '%logistics%'
            OR lower(display_title) LIKE '%driver%' OR lower(display_title) LIKE '%material%' OR lower(display_title) LIKE '%afe ops%' 
            OR lower(display_title) LIKE '%carrier%' OR lower(display_title) LIKE '%distribution%' OR lower(display_title) LIKE '%application tech%' 
            OR lower(display_title) LIKE '%tech %' THEN 'Information Technology'
        
        WHEN lower(display_title) LIKE '%accountant%' OR lower(display_title) LIKE '%accounting%' OR lower(display_title) LIKE '%payroll%'
            OR lower(display_title) LIKE '%finance%' OR lower(display_title) LIKE '%credit%' OR lower(display_title) LIKE '%a/r specialist%' OR 
            lower(display_title) LIKE '%billing%' OR lower(display_title) LIKE '%insurance%' OR lower(display_title) LIKE '%wealth %' OR 
            lower(display_title) LIKE '%mortgage%' OR lower(display_title) LIKE '%bank%' THEN 'Finance & Accounting'
        
        WHEN lower(display_title) LIKE '%guest %' OR lower(display_title) LIKE '%housekeep%' OR lower(display_title) LIKE '%caterin%' 
            OR lower(display_title) LIKE '%bart%' OR lower(display_title) LIKE '%barback%' OR lower(display_title) LIKE '%server%'
            OR lower(display_title) LIKE '%front desk%' OR lower(display_title) LIKE '%barista%' OR lower(display_title) LIKE '%room %'
            OR lower(display_title) LIKE '%attend%' OR lower(display_title) LIKE '%dining%' OR lower(display_title) LIKE '%reception%' THEN 'Hospitality'
        
        WHEN lower(display_title) LIKE '%attorn%' OR lower(display_title) LIKE '%paraleg%' OR lower(display_title) LIKE '%legal%' OR lower(display_title) LIKE '%public def%'
            OR lower(display_title) LIKE '%correction%' OR lower(display_title) LIKE '%court%' THEN 'Legal'
        
        WHEN lower(display_title) LIKE '%teach%' OR lower(display_title) LIKE '%academ%' OR lower(display_title) LIKE '%librar%' OR 
            lower(display_title) LIKE '%research%' OR lower(display_title) LIKE '%admiss%' OR lower(display_title) LIKE '%train%' THEN 'Education & Research'

        WHEN lower(display_title) LIKE '%administrativ%' OR lower(display_title) LIKE '%office%' OR lower(display_title) LIKE '%assist%' 
            OR lower(display_title) LIKE '%cashier%' OR lower(display_title) LIKE '%receiving%' OR lower(display_title) LIKE '%coordinat%' 
            OR lower(display_title) LIKE '%clerk%' OR lower(display_title) LIKE '%merchan%' OR lower(display_title) LIKE '%registrar%' 
            OR lower(display_title) LIKE '%manufactur%' OR lower(display_title) LIKE '%worker%' OR lower(display_title) LIKE '%printer%' THEN 'Administrative & Clerical'
        
        WHEN lower(display_title) LIKE '%maintenan%' OR lower(display_title) LIKE '%technici%' OR lower(display_title) LIKE '%mechanic%' 
            OR lower(display_title) LIKE '%janitor%' OR lower(display_title) LIKE '%labor%' OR lower(display_title) LIKE '%asphalt%' OR lower(display_title) LIKE '%crew%'
            OR lower(display_title) LIKE '%clean%' OR lower(display_title) LIKE '%house%' OR lower(display_title) LIKE '%housing%' OR lower(display_title) LIKE '%keeper%'
            OR lower(display_title) LIKE '%horticult%' OR lower(display_title) LIKE '%machine%' OR lower(display_title) LIKE '%parking%' 
            OR lower(display_title) LIKE '%securit%' THEN 'Maintenance & Skilled Labor'
        
        WHEN lower(display_title) LIKE '%human resource%' OR lower(display_title) LIKE '%hr %' OR lower(display_title) LIKE '%manage%' 
            OR lower(display_title) LIKE '%operat%' OR lower(display_title) LIKE '%retail%' OR lower(display_title) LIKE '%royalt%' OR lower(display_title) LIKE '%team m%'
            OR lower(display_title) LIKE '%team le%' THEN 'Other Business Function'
        
        ELSE 'Other'
    END;

