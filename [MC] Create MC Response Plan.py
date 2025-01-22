"""
The purpose of this playbook is to transfer custom SOAR workbooks over to MC as response plans.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'workbook_prompt' block
    workbook_prompt(container=container)

    return

@phantom.playbook_block()
def create_response_template(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("create_response_template() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ################################################################################
    # POST request to create MC response plan.
    ################################################################################

    parse_workbook_phases__json_body = json.loads(_ if (_ := phantom.get_run_data(key="parse_workbook_phases:json_body")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    parameters.append({
        "body": parse_workbook_phases__json_body,
        "location": "servicesNS/-/missioncontrol/v1/responsetemplates",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="create_response_template", assets=["agile-albatross-b6u.stg.splunkcloud.com"], callback=decision_3)

    return


@phantom.playbook_block()
def workbook_prompt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("workbook_prompt() called")

    ################################################################################
    # Enter workbook ID to copy into MC.
    ################################################################################

    # set approver and message variables for phantom.prompt call

    user = phantom.collect2(container=container, datapath=["playbook:launching_user.name"])[0][0]
    role = None
    message = """Enter the ID of the workbook you want to copy to Mission Control."""

    # parameter list for template variable replacement
    parameters = []

    # responses
    response_types = [
        {
            "prompt": "Workbook ID",
            "options": {
                "type": "range",
                "required": True,
                "min": 1,
                "max": 100,
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="workbook_prompt", parameters=parameters, response_types=response_types, callback=retrieve_workbook_details)

    return


@phantom.playbook_block()
def retrieve_workbook_details(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("retrieve_workbook_details() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    location_formatted_string = phantom.format(
        container=container,
        template="""rest/workbook_template/{0}""",
        parameters=[
            "workbook_prompt:action_result.summary.responses.0"
        ])

    ################################################################################
    # GET request to retrieve the workbook name and description.
    ################################################################################

    workbook_prompt_result_data = phantom.collect2(container=container, datapath=["workbook_prompt:action_result.summary.responses.0","workbook_prompt:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'retrieve_workbook_details' call
    for workbook_prompt_result_item in workbook_prompt_result_data:
        if location_formatted_string is not None:
            parameters.append({
                "location": location_formatted_string,
                "context": {'artifact_id': workbook_prompt_result_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get data", parameters=parameters, name="retrieve_workbook_details", assets=["soar_local"], callback=decision_1)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    ################################################################################
    # Check to see if request is successful.
    ################################################################################

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["retrieve_workbook_details:action_result.status", "==", "success"]
        ],
        delimiter=",")

    # call connected blocks if condition 1 matched
    if found_match_1:
        retrieve_workbook_phases(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    join_add_error_tag(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def retrieve_workbook_phases(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("retrieve_workbook_phases() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    location_formatted_string = phantom.format(
        container=container,
        template="""rest/workbook_phase_template?_filter_template_id={0}""",
        parameters=[
            "workbook_prompt:action_result.summary.responses.0"
        ])

    ################################################################################
    # GET request to retrieve the workbook phases.
    ################################################################################

    workbook_prompt_result_data = phantom.collect2(container=container, datapath=["workbook_prompt:action_result.summary.responses.0","workbook_prompt:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'retrieve_workbook_phases' call
    for workbook_prompt_result_item in workbook_prompt_result_data:
        if location_formatted_string is not None:
            parameters.append({
                "location": location_formatted_string,
                "context": {'artifact_id': workbook_prompt_result_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get data", parameters=parameters, name="retrieve_workbook_phases", assets=["soar_local"], callback=decision_2)

    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_2() called")

    ################################################################################
    # Check to see if request is successful.
    ################################################################################

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["retrieve_workbook_phases:action_result.status", "==", "success"]
        ],
        delimiter=",")

    # call connected blocks if condition 1 matched
    if found_match_1:
        parse_workbook_phases(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    join_add_error_tag(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def parse_workbook_phases(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("parse_workbook_phases() called")

    ################################################################################
    # Parse out phase name, description, and if a note is required. Does not currently 
    # parse out SLAs, playbooks, or actions. Sample request will be available in the 
    # repo with all available fields that can be added.
    ################################################################################

    retrieve_workbook_phases_result_data = phantom.collect2(container=container, datapath=["retrieve_workbook_phases:action_result.data.*.parsed_response_body"], action_results=results)
    retrieve_workbook_details_result_data = phantom.collect2(container=container, datapath=["retrieve_workbook_details:action_result.data.*.parsed_response_body.name","retrieve_workbook_details:action_result.data.*.parsed_response_body.description"], action_results=results)

    retrieve_workbook_phases_result_item_0 = [item[0] for item in retrieve_workbook_phases_result_data]
    retrieve_workbook_details_result_item_0 = [item[0] for item in retrieve_workbook_details_result_data]
    retrieve_workbook_details_result_item_1 = [item[1] for item in retrieve_workbook_details_result_data]

    parse_workbook_phases__json_body = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    # Create list to save each phase of a workbook
    phases = []
    
    # Iterate each phase in the workbook
    for phase in retrieve_workbook_phases_result_data[0][0]["data"]:
                        
        # Parse the workbook details
        phase_name = phase["name"]
        phase_order = phase["order"]
        phase_tasks = phase["tasks"]
        
        # Create list to save each task
        tasks = []
        
        # Iterate each task in a phase
        for task in phase_tasks:
            
            # Parse the task details
            task_name = task["name"]
            task_order = task["order"]
            task_description = task["description"]
            task_is_note_required = task["is_note_required"]
            
            if not task_description:
                task_description = "N/A"                        
            elif task_description == "":
                task_description = "N/A"
            elif task_description == "null":
                task_description = "N/A"
            # Remove double quotes and returns
            #task_description = task_description.replace('"',"'")            
            task_description = task_description.replace('"', '')
            task_description = task_description.replace('\'', '')
            task_description = task_description.replace('\n', '')
            task_description = task_description.replace('\r', '')
            
            # Save to task list
            tasks.append({"name":task_name,"order":task_order,"description":task_description,"is_note_required":task_is_note_required,"owner":"","suggestions":{"actions":[],"searches":[]},"start_time":0,"end_time":0,"total_time_taken":0})
        
        # Save to phase list
        phases.append({"name":phase_name,"order":phase_order,"tasks":tasks})
        
    workbook_name = retrieve_workbook_details_result_item_0[0]
    workbook_description = retrieve_workbook_details_result_item_1[0]    
    
    if not workbook_description:
        workbook_description = workbook_name
    elif workbook_description == "":
        workbook_description = workbook_name
    elif workbook_description == "null":
        workbook_description = workbook_name
    
    workbook_description = workbook_description.replace('"', '')
    workbook_description = workbook_description.replace('\'', '')
    workbook_description = workbook_description.replace('\n', '')
    workbook_description = workbook_description.replace('\r', '')
    
    # Create JSON body    
    #parse_workbook_phases__json_body = {"version":1,"is_default":False,"creator":"hatalla","update_by":"hatalla","name":retrieve_workbook_details_result_item_0[0],"description":retrieve_workbook_details_result_item_1[0],"template_status":"published","phases":phases}
    parse_workbook_phases__json_body = {"version":1,"is_default":False,"creator":"hatalla","update_by":"hatalla","name":workbook_name,"description":workbook_description,"template_status":"published","phases":phases}
    
    convert_json = json.dumps(parse_workbook_phases__json_body)
    phantom.debug(convert_json)
    
    parse_workbook_phases__json_body = convert_json

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="parse_workbook_phases:json_body", value=json.dumps(parse_workbook_phases__json_body))

    create_response_template(container=container)

    return


@phantom.playbook_block()
def decision_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_3() called")

    ################################################################################
    # Check to see if request is successful.
    ################################################################################

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["create_response_template:action_result.status", "==", "success"]
        ],
        delimiter=",")

    # call connected blocks if condition 1 matched
    if found_match_1:
        return

    # check for 'else' condition 2
    join_add_error_tag(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def join_add_error_tag(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_add_error_tag() called")

    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key="join_add_error_tag_called"):
        return

    # save the state that the joined function has now been called
    phantom.save_run_data(key="join_add_error_tag_called", value="add_error_tag")

    # call connected block "add_error_tag"
    add_error_tag(container=container, handle=handle)

    return


@phantom.playbook_block()
def add_error_tag(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_error_tag() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.add_tags(container=container, tags="error")

    container = phantom.get_container(container.get('id', None))

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