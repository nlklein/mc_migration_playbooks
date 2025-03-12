"""
This is an example playbook that will cancel any actions in the running state that were created more than 20 minutes ago.  It will prompt the administrator to confirm before canceling the actions.
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'datetime_now_minus_20_minutes' block
    datetime_now_minus_20_minutes(container=container)

    return

def get_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('get_data_1() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'get_data_1' call
    formatted_data_1 = phantom.get_format_data(name='format_action_run_REST_get_data')

    parameters = []
    
    # build parameters list for 'get_data_1' call
    parameters.append({
        'headers': "",
        'location': formatted_data_1,
        'verify_certificate': False,
    })

    phantom.act(action="get data", parameters=parameters, assets=['http_phantom_187'], callback=check_for_playbook_runs_found, name="get_data_1")

    return

def datetime_now_minus_20_minutes(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('datetime_now_minus_20_minutes() called')
    
    literal_values_0 = [
        [
            -20,
            "%Y-%m-%d %H:%M:%S",
        ],
    ]

    parameters = []

    for item0 in literal_values_0:
        parameters.append({
            'input_datetime': None,
            'amount_to_modify': item0[0],
            'modification_unit': None,
            'input_format_string': None,
            'output_format_string': item0[1],
        })
    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################    

    # call custom function "community/datetime_modify", returns the custom_function_run_id
    phantom.custom_function(custom_function='community/datetime_modify', parameters=parameters, name='datetime_now_minus_20_minutes', callback=format_action_run_REST_get_data)

    return

def format_action_run_REST_get_data(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_action_run_REST_get_data() called')
    
    template = """action_run?_filter_create_time__lte='{0}'&_filter_status=\"running\"&page_size=0&order=asc&sort=id"""

    # parameter list for template variable replacement
    parameters = [
        "datetime_now_minus_20_minutes:custom_function_result.data.datetime_string",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_action_run_REST_get_data", separator=", ")

    get_data_1(container=container)

    return

def format_action_run_REST_post_data(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_action_run_REST_post_data() called')
    
    template = """%%
action_run/{0}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "get_data_1:action_result.data.*.response_body.data.*.id",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_action_run_REST_post_data", separator=", ")

    post_data_1(container=container)

    return

def post_data_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('post_data_1() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'post_data_1' call
    formatted_data_1 = phantom.get_format_data(name='format_action_run_REST_post_data__as_list')

    parameters = []
    
    # build parameters list for 'post_data_1' call
    for formatted_part_1 in formatted_data_1:
        parameters.append({
            'body': "{\"cancel\":true}",
            'headers': "",
            'location': formatted_part_1,
            'verify_certificate': False,
        })

    phantom.act(action="post data", parameters=parameters, assets=['http_phantom_187'], callback=check_for_post_data_success, name="post_data_1")

    return

def prompt_admin_to_cancel(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_admin_to_cancel() called')
    
    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "format_prompt_message:formatted_data",
    ]

    #responses:
    response_types = [
        {
            "prompt": "",
            "options": {
                "type": "list",
                "choices": [
                    "Yes",
                    "No",
                ]
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_admin_to_cancel", separator=", ", parameters=parameters, response_types=response_types, callback=check_for_yes_response)

    return

def check_for_yes_response(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_for_yes_response() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["prompt_admin_to_cancel:action_result.summary.responses.0", "==", "Yes"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        format_action_run_REST_post_data(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    format_cancel_message(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def add_comment_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_comment_2() called')

    formatted_data_1 = phantom.get_format_data(name='format_cancel_message')

    phantom.comment(container=container, comment=formatted_data_1)

    return

def check_for_playbook_runs_found(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_for_playbook_runs_found() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["get_data_1:action_result.data.*.response_body.count", ">", 0],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        format_prompt_message(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    add_comment_3(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def add_comment_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_comment_3() called')

    phantom.comment(container=container, comment="No playbook runs were found that are in the \"running\" state that started > 20 minutes ago.")

    return

def format_prompt_message(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_prompt_message() called')
    
    template = """Please approve cancellation of the following actions:

Container, Action Run ID, Action, Create Time
%%
{0}, {1}, {2}, {3}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "get_data_1:action_result.data.*.response_body.data.*.container",
        "get_data_1:action_result.data.*.response_body.data.*.id",
        "get_data_1:action_result.data.*.response_body.data.*.action",
        "get_data_1:action_result.data.*.response_body.data.*.create_time",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_prompt_message", separator=", ")

    prompt_admin_to_cancel(container=container)

    return

def format_cancel_action_run_success(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_cancel_action_run_success() called')
    
    template = """The following action runs were successfully attempted to cancel

%%
{0}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "filtered-data:filter_for_post_data_success:condition_1:post_data_1:action_result.data.*.response_body.cancelled",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_cancel_action_run_success", separator=", ")

    add_comment_4(container=container)

    return

def check_for_post_data_success(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('check_for_post_data_success() called')

    # check for 'if' condition 1
    matched = phantom.decision(
        container=container,
        action_results=results,
        conditions=[
            ["post_data_1:action_result.status", "==", "success"],
        ])

    # call connected blocks if condition 1 matched
    if matched:
        filter_for_post_data_success(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)
        return

    # call connected blocks for 'else' condition 2
    format_post_data_error_message(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function)

    return

def filter_for_post_data_success(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('filter_for_post_data_success() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["post_data_1:action_result.status", "==", "success"],
        ],
        name="filter_for_post_data_success:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        format_cancel_action_run_success(action=action, success=success, container=container, results=results, handle=handle, custom_function=custom_function, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def add_comment_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_comment_4() called')

    formatted_data_1 = phantom.get_format_data(name='format_cancel_action_run_success')

    phantom.comment(container=container, comment=formatted_data_1)

    return

def format_post_data_error_message(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_post_data_error_message() called')
    
    template = """There was an error in the post data:

%%
Location: {0}
Message: {1}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "post_data_1:action_result.data.*.location",
        "post_data_1:action_result.message",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_post_data_error_message", separator=", ")

    add_comment_5(container=container)

    return

def add_comment_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_comment_5() called')

    formatted_data_1 = phantom.get_format_data(name='format_post_data_error_message')

    phantom.comment(container=container, comment=formatted_data_1)

    return

def format_cancel_message(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('format_cancel_message() called')
    
    template = """Analyst chose NOT to cancel the following actions:

Container, Action Run ID, Action, Create Time
%%
{0}, {1}, {2}, {3}
%%"""

    # parameter list for template variable replacement
    parameters = [
        "get_data_1:action_result.data.*.response_body.data.*.container",
        "get_data_1:action_result.data.*.response_body.data.*.id",
        "get_data_1:action_result.data.*.response_body.data.*.action",
        "get_data_1:action_result.data.*.response_body.data.*.create_time",
    ]

    phantom.format(container=container, template=template, parameters=parameters, name="format_cancel_message", separator=", ")

    add_comment_2(container=container)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return