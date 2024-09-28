alter table "_job_benefits" 
add column benefit_cluster varchar(255);

UPDATE _job_benefits
SET benefit_cluster = 
    CASE 
    	when lower(job_benefit_value) like '%401%' or lower(job_benefit_value) like '%403%' or lower(job_benefit_value) like '%457%' or lower(job_benefit_value)  like '%retirement%'
    	then 'Retirement Plant'
    	
    	when lower(job_benefit_value) like '%stock%' or lower(job_benefit_value) like '%profit%' or lower(job_benefit_value) like '%loan%' or lower(job_benefit_value) like '%credit%'
    	or lower(job_benefit_value) like '%saving%' then 'Financial Benefits'
    	
    	when lower(job_benefit_value) like '%dental%' or lower(job_benefit_value) like '%vision%' or lower(job_benefit_value) like '%disabilit%' 
    	or lower(job_benefit_value) like '%smokin%' or lower(job_benefit_value) like '%health%' or lower(job_benefit_value) like '%gym%' or lower(job_benefit_value) like '%fitness%'
    	or lower(job_benefit_value) like '%wellness%' or lower(job_benefit_value) like '%pet %' then 'Healthcare & Wellness'
    	
    	when lower(job_benefit_value) like '%visa%' or lower(job_benefit_value) like '%sponsor%' or lower(job_benefit_value) like '%immigrat%' then 'Immigration & Visa Support'
    	
    	when lower(job_benefit_value) like '%holiday%' or lower(job_benefit_value) like '%leave%' or lower(job_benefit_value) like '%flexible%' 
    	or lower(job_benefit_value) like '%parental%' or lower(job_benefit_value) like '%sick%' or lower(job_benefit_value) like '%time off%'
    	or lower(job_benefit_value) like '%bereavement%' or lower(job_benefit_value) like '%work from home%' then 'Time Off & Flexibility'
    	
    	when lower(job_benefit_value) like '%relocation%' or lower(job_benefit_value) like '%travel%' or lower(job_benefit_value) like '%mileage%'
    	or lower(job_benefit_value) like '%commuter%' or lower(job_benefit_value) like '%parking%' or lower(job_benefit_value) like '%fuel%'
    	then 'Relocation & Commuting'
    	
    	when lower(job_benefit_value) like '%education%' or  lower(job_benefit_value) like '%training%' or lower(job_benefit_value) like '%professio%' 
    	or lower(job_benefit_value) like '%developme%' or lower(job_benefit_value) like '%on-the-job%' or lower(job_benefit_value) like '%on the job%'
    	or lower(job_benefit_value) like '%leaders%' or lower(job_benefit_value) like '%tuition%' or lower(job_benefit_value) like '%orientat%'
    	or lower(job_benefit_value) like '%advance%' or lower(job_benefit_value) like '%assist%' then 'Learning & Development'
    	
    	when lower(job_benefit_value) like '%discount%' or lower(job_benefit_value) like '%benefit%' or lower(job_benefit_value) like '%partner%' 
    	or lower(job_benefit_value) like '%reimburse%' or lower(job_benefit_value) like '%food%' or lower(job_benefit_value) like '%happy hour%' 
    	or lower(job_benefit_value) like '%happy-hour%' or lower(job_benefit_value) like '%free%' then 'Discounts & Perks'
    	
    	when lower(job_benefit_value) like '%from-home%' or lower(job_benefit_value) like '%from home%' or lower(job_benefit_value) like '%remote%'
    	then 'Workplace Flexibility'
    	
    	when lower(job_benefit_value) like '%insuran%' or lower(job_benefit_value) like '%ad&d%' or lower(job_benefit_value) like '%assur%' 
    	then 'Other Insurance'

    	else 'Other'
   end;
