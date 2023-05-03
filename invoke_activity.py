from invokes import invoke_http

def activity_log(log_info):
    '''
    This function invokes activity log microservice everytime an MS is invoked or error encountered
    input: microservice_name OR microservice_name_error OR function_error
    output: none, this is a fire forget microservice
    '''
    activity = "http://localhost:1114/create_log"
    log_json = {
        "log_info":log_info
    }
    invoke_http(activity,method='POST',json=log_json)