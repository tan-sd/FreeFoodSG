from invokes import invoke_http

def activity_log(ms_name):
    '''
    This function invokes activity log microservice everytime an MS is invoked
    input: microservice_name OR microservice_name_error
    output: none, this is a fire forget microservice
    '''
    activity = "http://localhost:1114/create_log"
    ms_json = {
        "ms_invoked":ms_name
    }
    invoke_http(activity,method='POST',json=ms_json)