"""
The purpose of this playbook is to add the SOAR container ID to the MC incident description and then add the MC ID to the SOAR container as an artifact.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'get_description' block
    get_description(container=container)
    # call 'save_mc_id_to_container' block
    save_mc_id_to_container(container=container)

    return

@phantom.playbook_block()
def get_description(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_description() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Get current incident description.
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

    phantom.act("get incident", parameters=parameters, name="get_description", assets=["builtin_mc_connector"], callback=add_container_id_to_description)

    return


@phantom.playbook_block()
def add_container_id_to_description(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("add_container_id_to_description() called")

    ################################################################################
    # Append SOAR container ID to the bottom of the description.
    ################################################################################

    template = """{0}\n\nSOAR Container ID: {1}"""

    # parameter list for template variable replacement
    parameters = [
        "get_description:action_result.data.*.description",
        "container:id"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="add_container_id_to_description")

    update_incident_description(container=container)

    return


@phantom.playbook_block()
def update_incident_description(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("update_incident_description() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # Update incident description in MC.
    ################################################################################

    external_id_value = container.get("external_id", None)
    add_container_id_to_description = phantom.get_format_data(name="add_container_id_to_description")

    parameters = []

    if external_id_value is not None:
        parameters.append({
            "description": add_container_id_to_description,
            "incident_id": external_id_value,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update incidents", parameters=parameters, name="update_incident_description", assets=["builtin_mc_connector"])

    return


@phantom.playbook_block()
def save_mc_id_to_container(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("save_mc_id_to_container() called")

    ################################################################################
    # Save MC incident ID to SOAR container as artifact.
    ################################################################################

    external_id_value = container.get("external_id", None)
    id_value = container.get("id", None)

    parameters = []

    parameters.append({
        "name": "Mission Control ID",
        "tags": None,
        "label": None,
        "severity": None,
        "cef_field": "mc_id",
        "cef_value": external_id_value,
        "container": id_value,
        "input_json": None,
        "cef_data_type": None,
        "run_automation": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/artifact_create", parameters=parameters, name="save_mc_id_to_container")

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