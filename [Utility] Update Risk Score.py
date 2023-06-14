"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'filter_1' block
    filter_1(container=container)

    return

@phantom.playbook_block()
def format_risk_score_spl(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_risk_score_spl() called")

    template = """| makeresults | eval dest=\"example.splunkcloud.com\"\n| sendalert risk param._risk_object=dest param._risk_object_type=\"system\" param._risk_score={0}"""

    # parameter list for template variable replacement
    parameters = [
        "map_vt_score_with_rba_score:custom_function:rba_score"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_risk_score_spl")

    update_risk_score(container=container)

    return


@phantom.playbook_block()
def update_risk_score(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("update_risk_score() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    format_risk_score_spl = phantom.get_format_data(name="format_risk_score_spl")

    parameters = []

    if format_risk_score_spl is not None:
        parameters.append({
            "query": format_risk_score_spl,
            "command": "",
            "search_mode": "smart",
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("run query", parameters=parameters, name="update_risk_score", assets=["splunk-external"])

    return


@phantom.playbook_block()
def get_filehash_score_from_vt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("get_filehash_score_from_vt() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.fileHash","artifact:*.id"])

    parameters = []

    # build parameters list for 'get_filehash_score_from_vt' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
            parameters.append({
                "hash": container_artifact_item[0],
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("file reputation", parameters=parameters, name="get_filehash_score_from_vt", assets=["hani_vt"], callback=map_vt_score_with_rba_score)

    return


@phantom.playbook_block()
def map_vt_score_with_rba_score(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("map_vt_score_with_rba_score() called")

    get_filehash_score_from_vt_result_data = phantom.collect2(container=container, datapath=["get_filehash_score_from_vt:action_result.data.*.attributes.reputation"], action_results=results)

    get_filehash_score_from_vt_result_item_0 = [item[0] for item in get_filehash_score_from_vt_result_data]

    map_vt_score_with_rba_score__rba_score = None
    map_vt_score_with_rba_score__virus_total_score = None

    ################################################################################
    ## Custom Code Start
    ################################################################################
    
    phantom.debug("actual filehash reputation from VT: {}".format(get_filehash_score_from_vt_result_item_0[0]))
    
    ############################################
    ### Using a static Virus Total reputation score of -50 as an example instead of using get_filehash_score_from_vt_result_item_0
    ### Will need to grab actual value from Virus Total Response    
    ### you can uncomment the following line to search for the actual reputation score in the custom list
    ### virus_total_repuation = get_filehash_score_from_vt_result_item_0[0]
    ############################################
        
    ############################################
    virus_total_reputation = "-50"
    ############################################
    
    get_rba_score = ""
    success, message, rba_score_list = phantom.get_list(list_name='virus_total_score_rba_mapping')
    phantom.debug("success: {}, message: {}, rba_score_list: {}".format(success, message, rba_score_list))
    
    if success==True and len(rba_score_list) > 0:
        for virus_total_score, rba_score in rba_score_list:
            phantom.debug("virus_total_score: {}, rba_score: {}".format(str(virus_total_score), str(rba_score)))
            if virus_total_reputation in str(virus_total_score):
                get_rba_score = rba_score
                break
    
    
    map_vt_score_with_rba_score__virus_total_score = virus_total_reputation
    map_vt_score_with_rba_score__rba_score = get_rba_score
    
    phantom.debug("filehash VT reputation score: {}".format(map_vt_score_with_rba_score__virus_total_score))
    phantom.debug("matching RBA score: {}".format(map_vt_score_with_rba_score__rba_score))
        
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_run_data(key="map_vt_score_with_rba_score:rba_score", value=json.dumps(map_vt_score_with_rba_score__rba_score))
    phantom.save_run_data(key="map_vt_score_with_rba_score:virus_total_score", value=json.dumps(map_vt_score_with_rba_score__virus_total_score))

    format_add_enrichment_artifact(container=container)

    return


@phantom.playbook_block()
def add_artifact_with_risk_scores(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("add_artifact_with_risk_scores() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    source_data_identifier_value = container.get("source_data_identifier", None)
    format_add_enrichment_artifact = phantom.get_format_data(name="format_add_enrichment_artifact")

    parameters = []

    if source_data_identifier_value is not None:
        parameters.append({
            "name": "enrichment",
            "label": "Scores",
            "cef_dictionary": format_add_enrichment_artifact,
            "source_data_identifier": source_data_identifier_value,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add artifact", parameters=parameters, name="add_artifact_with_risk_scores", assets=["soar_internal"], callback=format_risk_score_spl)

    return


@phantom.playbook_block()
def format_add_enrichment_artifact(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("format_add_enrichment_artifact() called")

    template = """{{\"rba_score\":\"{0}\",\"virus_total_score\":\"{1}\"}}"""

    # parameter list for template variable replacement
    parameters = [
        "map_vt_score_with_rba_score:custom_function:rba_score",
        "map_vt_score_with_rba_score:custom_function:virus_total_score"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_add_enrichment_artifact")

    add_artifact_with_risk_scores(container=container)

    return


@phantom.playbook_block()
def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug("filter_1() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["artifact:*.cef.fileHash", "!=", ""]
        ],
        name="filter_1:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        get_filehash_score_from_vt(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

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