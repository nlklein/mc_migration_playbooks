"""
The purpose of this playbook is to ingest on poll SOAR containers into MC as incidents. The SOAR container artifacts are then saved to the MC incident as events.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'create_incident' block
    create_incident(container=container)

    return

@phantom.playbook_block()
def create_incident(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("create_incident() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    name_formatted_string = phantom.format(
        container=container,
        template="""SOAR Poll - {0}\n""",
        parameters=[
            "container:name"
        ])

    ################################################################################
    # Create Mission Control incident for the new on poll container.
    ################################################################################

    name_value = container.get("name", None)

    parameters = []

    if name_formatted_string is not None:
        parameters.append({
            "name": name_formatted_string,
            "status": "New",
            "description": "This incident was created from SOAR on-poll demo.",
            "incident_type": "soar_poll",
            "incident_origin": "",
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("create incidents", parameters=parameters, name="create_incident", assets=["builtin_mc_connector"], callback=save_mc_id_as_artifact)

    return


@phantom.playbook_block()
def save_mc_id_as_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("save_mc_id_as_artifact() called")

    ################################################################################
    # Save the new MC incident ID to the container as an artifact.
    ################################################################################

    id_value = container.get("id", None)
    create_incident_result_data = phantom.collect2(container=container, datapath=["create_incident:action_result.data.*.id","create_incident:action_result.parameter.context.artifact_id","create_incident:action_result.parameter.context.artifact_external_id"], action_results=results)

    parameters = []

    # build parameters list for 'save_mc_id_as_artifact' call
    for create_incident_result_item in create_incident_result_data:
        parameters.append({
            "name": "Created Mission ID",
            "tags": None,
            "label": "info",
            "severity": "Informational",
            "cef_field": "mc_id",
            "cef_value": create_incident_result_item[0],
            "container": id_value,
            "input_json": None,
            "cef_data_type": None,
            "run_automation": False,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/artifact_create", parameters=parameters, name="save_mc_id_as_artifact", callback=iterate_all_artifacts)

    return


@phantom.playbook_block()
def close_container(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("close_container() called")

    ################################################################################
    # Close current container. A new container will automatically be created and linked 
    # to the new MC incident.
    ################################################################################

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.set_status(container=container, status="closed")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def add_comment(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("add_comment() called")

    ################################################################################
    # On-poll container successfully moved to Mission Control. Closing container.
    ################################################################################

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="On-poll container successfully moved to Mission Control. Closing container.")

    close_container(container=container)

    return


@phantom.playbook_block()
def iterate_all_artifacts(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("iterate_all_artifacts() called")

    ################################################################################
    # Iterate all artifacts in the current container and create JSON body for the 
    # POST request.
    ################################################################################

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef"])
    create_incident_result_data = phantom.collect2(container=container, datapath=["create_incident:action_result.data.*.id"], action_results=results)

    container_artifact_header_item_0 = [item[0] for item in container_artifact_data]
    create_incident_result_item_0 = [item[0] for item in create_incident_result_data]

    iterate_all_artifacts__http_body = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    # DECLARE EVENT LIST
    iterate_all_artifacts__http_body = []
    
    # ITERATE ARTIFACTS IN CONTAINER
    for artifact in container_artifact_data:
        
        # SAVE DICTIONARY TO REFERNCE IN FOR LOOP
        dictionary = artifact[0]

        # ITERATE CEF FIELDS
        for field in artifact[0]:
            
            # RETRIEVE CEF VALUE
            field_value = None
            field_value = dictionary[field]
            
            # IF VALUE PRESENT, CONTINUE 
            if field_value:
                phantom.error(field)
                phantom.error(field_value)
                
                field_json = '{"' + str(field) + '":"' + str(field_value) + '"}'
                iterate_all_artifacts__http_body.append(field_json)
                
            


    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="iterate_all_artifacts:http_body", value=json.dumps(iterate_all_artifacts__http_body))

    iterate_http_body(container=container)

    return


@phantom.playbook_block()
def iterate_http_body(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("iterate_http_body() called")

    ################################################################################
    # Iterate all JSON requests.
    ################################################################################

    template = """%%\n{0}\n%%"""

    # parameter list for template variable replacement
    parameters = [
        "iterate_all_artifacts:custom_function:http_body"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="iterate_http_body")

    create_mc_event(container=container)

    return


@phantom.playbook_block()
def create_mc_event(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("create_mc_event() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    location_formatted_string = phantom.format(
        container=container,
        template="""v1/incidents/{0}/events\n""",
        parameters=[
            "create_incident:action_result.data.*.id"
        ])

    ################################################################################
    # Create MC events for each artifact.
    ################################################################################

    create_incident_result_data = phantom.collect2(container=container, datapath=["create_incident:action_result.data.*.id","create_incident:action_result.parameter.context.artifact_id","create_incident:action_result.parameter.context.artifact_external_id"], action_results=results)
    iterate_http_body__as_list = phantom.get_format_data(name="iterate_http_body__as_list")

    parameters = []

    # build parameters list for 'create_mc_event' call
    for iterate_http_body__item in iterate_http_body__as_list:
        for create_incident_result_item in create_incident_result_data:
            if location_formatted_string is not None:
                parameters.append({
                    "body": iterate_http_body__item,
                    "location": location_formatted_string,
                    "context": {'artifact_id': create_incident_result_item[1], 'artifact_external_id': create_incident_result_item[2]},
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="create_mc_event", assets=["local mission control"], callback=add_comment)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return