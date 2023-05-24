# mc_migration_playbooks
Playbooks made for Splunk .conf23 session SEC1226B that assist with moving existing SOAR customers to Mission Control.

Playbook 1 - [MC] Save Container ID to Incident
Description: The purpose of this playbook is to add the SOAR container ID to the MC incident description and then add the MC ID to the SOAR container as an artifact.
Setup: No asset configuration is necessary. Simply run playbook on containers that are created by MC. 

Playbook 2 - [MC] Create Incident from Container
Description: The purpose of this playbook is to ingest on poll SOAR containers into MC as incidents. The SOAR container artifacts are then saved to the MC incident as events.
Setup: (1) Provision an HTTP asset to create POST requests to MC. (2) Create a new incident type in MC for these incidents. In this playbook examples, we use "soar_poll" as the incident type.

Playbook 3 - [MC] Save MC Summary Fields to Container
Description: The purpose of this playbook is to add the summary fields from an MC incident to a SOAR container as artifacts.
Setup: Provision the Phantom app with local credentials.

Playbook 4 - [MC] Create MC Response Plan
Description: The purpose of this playbook is to transfer custom SOAR workbooks over to MC as response plans.
Setup: (1) Provision an HTTP asset to create POST requests to MC. (2) Provision an HTTP asset to perform GET request to SOAR.
Enhancements: This example playbook will transfer workbook name, workbook description, phase name, description, and if a note is required. It can be easily enhanced to parse out SLA, playbooks, and actions. A sample POST request can be found below:

{
  "version": 0,
  "is_default": true,
  "name": "string",
  "description": "string",
  "template_status": "string",
  "creator": "string",
  "updated_by": "string",
  "phases": [
    {
      "name": "string",
      "order": 0,
      "template_id": "string",
      "tasks": [
        {
          "name": "string",
          "order": 0,
          "description": "string",
          "phase_id": "string",
          "owner": "string",
          "suggestions": {
            "actions": [
              {
                "name": "geolocate ip - MaxMind",
                "type": "geolocate ip",
                "last_job_id": 0,
                "action": "1394",
                "appId": 169,
                "asset": 1,
                "parameters": [
                  {
                    "ip": "1.1.1.1"
                  }
                ],
                "update_time": 1676495407.1743503,
                "create_time": 1676495280.719768
              }
            ],
            "playbooks": [
              {
                "last_job_id": 0,
                "playbook_id": "community/suspicious_email_domain_enrichment",
                "name": "suspicious_email_domain_enrichment",
                "scope": "all",
                "update_time": 1676495407.17426,
                "create_time": 1676495280.719677
              }
            ],
            "searches": [
              {
                "name": "Access - Access Over Time By App",
                "spl": "%7C%20%60tstats%60%20count%20from%20datamodel%3DAuthentication.Authentication%20by%20_time%2CAuthentication.app%20span%3D10m%20%7C%20timechart%20minspan%3D10m%20useother%3D%60useother%60%20count%20by%20Authentication.app",
                "description": "Use Splunk searches to list the stats for app accessing",
                "update_time": 1676496024.7015831,
                "create_time": 1676495280.719843
              }
            ]
          }
        }
      ]
    }
  ]
}
