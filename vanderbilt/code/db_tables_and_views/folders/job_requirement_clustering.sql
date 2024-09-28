alter table "_job_requirements" 
add column requirement_cluster VARCHAR(255);

update _job_requirements
set requirement_cluster = 
case 
	when lower(job_requirement_name) like '%customer ser%' or lower(job_requirement_name) like '%call cent%'
	or lower(job_requirement_name) like '%guest serv%' or lower(job_requirement_name) like '%support%'
	or lower(job_requirement_name) like '%front desk%' then 'Customer Service & Support'
	
	when lower(job_requirement_name) like '%driver%' or lower(job_requirement_name) like '%cdl%' 
	or lower(job_requirement_name) like '%driving%' or lower(job_requirement_name) like '%transport%' 
	or lower(job_requirement_name) like '%dispatch%' then 'Driving & Transportation'
	
	when lower(job_requirement_name) like '%pos %' or lower(job_requirement_name) like '%cash handling%'
	or lower(job_requirement_name) like '%cash register%' or lower(job_requirement_name) like '%sales%'
	or lower(job_requirement_name) like '%shop%' or lower(job_requirement_name) like '%retail%' then 'Retail & Sales'
	
	when lower(job_requirement_name) like '%hospitality%' or lower(job_requirement_name) like '%hotel%' 
	or lower(job_requirement_name) like '%banquet%' or lower(job_requirement_name) like '%restaurant%' 
	or lower(job_requirement_name) like '%bar%' or lower(job_requirement_name) like '%food%'
	or lower(job_requirement_name) like '%servi%' then 'Hospitality & Food Service'
	
	when lower(job_requirement_name) like '%forklift%' or lower(job_requirement_name) like '%warehouse%' 
	or lower(job_requirement_name) like '%pallet%' or lower(job_requirement_name) like '%jack%'
	or lower(job_requirement_name) like '%material%' or lower(job_requirement_name) like '%handling%' or lower(job_requirement_name) like '%distribution%'
	or lower(job_requirement_name) like '%3pl%' then 'Warehouse & Material Handling'
	
	when lower(job_requirement_name) like '%microsoft%' or lower(job_requirement_name) like '%excel%'
	or lower(job_requirement_name) like '%office%' or lower(job_requirement_name) like '%outlook%' or lower(job_requirement_name) like '%suite%'
	or lower(job_requirement_name) like '%computer%' or lower(job_requirement_name) like '%as400%' or lower(job_requirement_name) like '%ethernet%'
	or lower(job_requirement_name) like '%cabling%' then 'Technology & Office Software'
	
	when lower(job_requirement_name) like '%medical%' or lower(job_requirement_name) like '%patient%' 
	or lower(job_requirement_name) like '%pharma%' or lower(job_requirement_name) like '%nursin%' or lower(job_requirement_name) like '%care%'
	or lower(job_requirement_name) like '%health%' or lower(job_requirement_name) like '%veterin%' or lower(job_requirement_name) like '%vital%'
	or lower(job_requirement_name) like '%emr %' or lower(job_requirement_name) like '%ehr %' or lower(job_requirement_name) like '%practice provider%'
	or lower(job_requirement_name) like '%nurse%' or lower(job_requirement_name) like '%medication%' or lower(job_requirement_name) like '%spinal%'
	or lower(job_requirement_name) like '%physiol%' then 'Healthcare & Medical'

	when lower(job_requirement_name) like '%leadersh%' or lower(job_requirement_name) like '%manage%' or lower(job_requirement_name) like '%teamwor%'
	or lower(job_requirement_name) like '%supervis%' or lower(job_requirement_name) like '%ambition%' then 'Leadership & Management'
	
	when lower(job_requirement_name) like '%license%' or lower(job_requirement_name) like '%certification%' or lower(job_requirement_name) like '%permit%'
	or lower(job_requirement_name) like '%permit%' then 'Licenses & Certifications'
	
	when lower(job_requirement_name) like '%educat%' or lower(job_requirement_name) like '%bachelor%' or lower(job_requirement_name) like '%undergrad%'
	or lower(job_requirement_name) like '%graduate%' or lower(job_requirement_name) like '%master%' or lower(job_requirement_name) like '%post-grad%' 
	or lower(job_requirement_name) like '%post grad%' or lower(job_requirement_name) like '%doctorat%' or lower(job_requirement_name) like '%phd%'
	or lower(job_requirement_name) like '%degree%' or lower(job_requirement_name) like '%high school%' or lower(job_requirement_name) like '%math%'
	then 'Education'
	
	when  lower(job_requirement_name) like '%legal%' or lower(job_requirement_name) like '%law%' or lower(job_requirement_name) like '%litigation%'
	or lower(job_requirement_name) like '%immigration%' or lower(job_requirement_name) like '%icd-10%' or lower(job_requirement_name) like '%icd10%'
	or lower(job_requirement_name) like '%fair hous%' then 'Legal & Compliance'
	
	when lower(job_requirement_name) like '%hand tool%' or lower(job_requirement_name) like '%repair%'
	or lower(job_requirement_name) like '%lifting%' or lower(job_requirement_name) like '%manufactur%' 
	or lower(job_requirement_name) like '%assembl%' or lower(job_requirement_name) like '%mainten%'
	then 'Manufacturing & Manual Labor'
	
	when lower(job_requirement_name) like '%creativ%' or lower(job_requirement_name) like '%photogr%' or lower(job_requirement_name) like '%writin%'
	or lower(job_requirement_name) like '% writer%'	or lower(job_requirement_name) like '%product demo%' or lower(job_requirement_name) like '%copywr%'
	then 'Creative Skills'
	
	when lower(job_requirement_name) like '%biling%' or lower(job_requirement_name) like '%spanis%' or lower(job_requirement_name) like '%englis%'
	or lower(job_requirement_name) like '%languag%' then 'Languages'
	
	when lower(job_requirement_name) like '%data entry%' or lower(job_requirement_name) like '%typing%' or lower(job_requirement_name) like '%phone etiquette%'
	or lower(job_requirement_name) like '%administrative%' or lower(job_requirement_name) like '%phone syst%'
	then 'Administrative Skills'
	
	when lower(job_requirement_name) like '%accounting%' or lower(job_requirement_name) like '%quickbooks%' 
	or lower(job_requirement_name) like '%math%' or lower(job_requirement_name) like '%insurance%' 
	 then 'Accounting & Finance'
	
	when lower(job_requirement_name) like '%shift%' or lower(job_requirement_name) like '%availability%' then 'Shift & Scheduling Arrangements'
	
	when lower(job_requirement_name) like '%research%' or lower(job_requirement_name) like '%analysis%' or lower(job_requirement_name) like '%gis%'
	then 'Research & Analysis'
	
	when lower(job_requirement_name) like '%integrity%' or lower(job_requirement_name) like '%interpersonal%' or lower(job_requirement_name) like '%social%'
	or lower(job_requirement_name) like '%negotiat%' or lower(job_requirement_name) like '%counseling%' or lower(job_requirement_name) like '%improvement%'
	or lower(job_requirement_name) like '%organizational%' then 'Interpersonal & Social / Soft Skills'
	
	when lower(job_requirement_name) like '%engineer%' or lower(job_requirement_name) like '%manufactur%' or lower(job_requirement_name) like '%automotive%'
	or lower(job_requirement_name) like '%diagnostics%' or lower(job_requirement_name) like '%ctr%' then 'Technical & Engineering'

	else 'Other'
	
end;

