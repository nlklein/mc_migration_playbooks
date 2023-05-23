"""
The purpose of this playbook is to add the summary fields from an MC incident to a SOAR container as artifacts.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_incident_details' block
    get_incident_details(container=container)

    return

@phantom.playbook_block()
def get_incident_details(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_incident_details() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Retrieve MC incident details.
    ################################################################################

    external_id_value = container.get("external_id", None)

    parameters = []

    if external_id_value is not None:
        parameters.append({
            "id": external_id_value,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get incident", parameters=parameters, name="get_incident_details", assets=["builtin_mc_connector"], callback=parse_incident_results)

    return


@phantom.playbook_block()
def parse_incident_results(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("parse_incident_results() called")

    ################################################################################
    # Parse summary fields from incident details.
    ################################################################################

    get_incident_details_result_data = phantom.collect2(container=container, datapath=["get_incident_details:action_result.data.*.summary"], action_results=results)

    get_incident_details_result_item_0 = [item[0] for item in get_incident_details_result_data]

    parse_incident_results__json_output = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
        
    dictionary = get_incident_details_result_data[0][0]
    
    output_list = []

    for field in get_incident_details_result_data[0][0]:
        field_value = dictionary[field]
        dictionary_format = '{"' + field + '":"' + str(field_value) + '"}'
        output_list.append(dictionary_format)
            
    parse_incident_results__json_output = output_list
    
    phantom.error(parse_incident_results__json_output)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="parse_incident_results:json_output", value=json.dumps(parse_incident_results__json_output))

    iterate_python_list(container=container)

    return


@phantom.playbook_block()
def add_artifacts_to_container(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("add_artifacts_to_container() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Add summary fields to container as artifacts.
    ################################################################################

    id_value = container.get("id", None)
    source_data_identifier_value = container.get("source_data_identifier", None)
    iterate_python_list__as_list = phantom.get_format_data(name="iterate_python_list__as_list")

    parameters = []

    # build parameters list for 'add_artifacts_to_container' call
    for iterate_python_list__item in iterate_python_list__as_list:
        if source_data_identifier_value is not None:
            parameters.append({
                "name": "MC Summary Field",
                "label": "MC",
                "cef_name": "",
                "cef_value": "",
                "container_id": id_value,
                "cef_dictionary": iterate_python_list__item,
                "source_data_identifier": source_data_identifier_value,
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add artifact", parameters=parameters, name="add_artifacts_to_container", assets=["soar_local"])

    return


@phantom.playbook_block()
def iterate_python_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("iterate_python_list() called")

    ################################################################################
    # Iterate the summary fields.
    ################################################################################

    template = """%%\n{0}\n%%"""

    # parameter list for template variable replacement
    parameters = [
        "parse_incident_results:custom_function:json_output"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="iterate_python_list")

    add_artifacts_to_container(container=container)

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