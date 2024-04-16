import re 


def param_extract(response_text, extraction_level, blacklisted_words, parameter_placeholder):

    ''' 
    regexp : r'.*?:\/\/.*\?.*\=[^$]'
    regexp : r'.*?:\/\/.*\?.*\='
    '''

    parameter_matches = list(set(re.findall(r'.*?:\/\/.*\?.*\=[^$]' , response_text)))
    extracted_parameters = []
        
    for parameter in parameter_matches:
        parameter_delimiter = parameter.find('=')
        second_parameter_delimiter = parameter.find('=', parameter.find('=') + 1)
        if len(blacklisted_words) > 0:
            blacklisted_words_regex = re.compile("|".join(blacklisted_words))
            if not blacklisted_words_regex.search(parameter):
                extracted_parameters.append((parameter[:parameter_delimiter+1] + parameter_placeholder))
                if extraction_level == 'high':
                    extracted_parameters.append(parameter[:second_parameter_delimiter+1] + parameter_placeholder)
        else:
            extracted_parameters.append((parameter[:parameter_delimiter+1] + parameter_placeholder))
            if extraction_level == 'high':
                extracted_parameters.append(parameter[:second_parameter_delimiter+1] + parameter_placeholder)

    return list(set(extracted_parameters))
