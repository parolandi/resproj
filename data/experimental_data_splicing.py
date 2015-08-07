
import data.data_splicing as dds
import models.model_data as mmd


'''
pseudo_exp: data.data_splicing.calib_valid_data
returns: models.model_data.calib_valid_experimental_dataset
'''
def convert_pseudo_experimental_to_experimental(pseudo_exp):
    exp = dict(mmd.calib_valid_experimental_dataset)
    exp["id"] = pseudo_exp["id"]
    calib = dict(mmd.experimental_dataset)
    calib["time"] = pseudo_exp["calib"]["time"]
    calib["observables"] = pseudo_exp["calib"]["meas"]
    exp["calib"] = calib
    valid = dict(mmd.experimental_dataset)
    valid["time"] = pseudo_exp["valid"]["time"]
    valid["observables"] = pseudo_exp["valid"]["meas"]
    exp["valid"] = valid
    return exp


'''
data:    list containing time and measurements, respectively
returns: calib_valid_experimental_dataset
'''
def splice_raw_data_with_pattern_111111(data):
    dataset = dict(mmd.calib_valid_experimental_dataset)
    dataset["calib"]["time"] = data[0]
    dataset["calib"]["observables"] = data[1:]
    dataset["id"] = dds.format_dataset_id("111111", str(len(data)))
    # WIP: add warning on diff len()
    return dataset


'''
data:    list containing time and measurements, respectively
returns: calib_valid_experimental_dataset
'''
def splice_raw_data_with_pattern_111000(data):
    dataset = dds.splice_data_with_pattern(dds.splice_data_with_pattern_111000_get_ones, \
        dds.splice_data_with_pattern_111000_get_zeros, data[0], data[1:], None, None)
    dataset["id"] = dds.format_dataset_id("111000", str(len(data)))
    # WIP: add warning on diff len()
    return convert_pseudo_experimental_to_experimental(dataset)


'''
data:    list containing time and measurements, respectively
returns: calib_valid_experimental_dataset
'''
def splice_raw_data_with_pattern_000111(data):
    dataset = dds.splice_data_with_pattern(dds.splice_data_with_pattern_000111_get_ones, \
        dds.splice_data_with_pattern_000111_get_zeros, data[0], data[1:], None, None)
    dataset["id"] = dds.format_dataset_id("000111", str(len(data)))
    # WIP: add warning on diff len()
    return convert_pseudo_experimental_to_experimental(dataset)


def splice_raw_data_with_pattern_multistage_yesyesno(data):
    """
    data:    list containing time and measurements, respectively
    returns: calib_valid_experimental_dataset
    """
    yesyesno = [15] # 15+15
    dataset = dds.splice_data_with_pattern_any(yesyesno, data[0], data[1:])
    dataset["id"] = dds.format_dataset_id("yesyesno", str(len(data)))                         
    return convert_pseudo_experimental_to_experimental(dataset)


def splice_raw_data_with_pattern_multistage_yes10yes15no5(data):
    """
    data:    list containing time and measurements, respectively
    returns: calib_valid_experimental_dataset
    """
    yes10yes15no5 = [25] # 25+5
    dataset = dds.splice_data_with_pattern_any(yes10yes15no5, data[0], data[1:])
    dataset["id"] = dds.format_dataset_id("yes10yes15no5", str(len(data)))                         
    return convert_pseudo_experimental_to_experimental(dataset)
    
    
def splice_raw_data_with_pattern_multistage_yesnoyes(data):
    """
    data:    list containing time and measurements, respectively
    returns: calib_valid_experimental_dataset
    """
    yesnoyes = [10,15] # 25+5
    dataset = dds.splice_data_with_pattern_any(yesnoyes, data[0], data[1:])
    dataset["id"] = dds.format_dataset_id("yesnoyes", str(len(data)))                         
    return convert_pseudo_experimental_to_experimental(dataset)


def splice_raw_data_with_pattern_multistage_yes15no5yes10(data):
    """
    data:    list containing time and measurements, respectively
    returns: calib_valid_experimental_dataset
    """
    yes15no5yes10 = [15,20] # 25+5
    dataset = dds.splice_data_with_pattern_any(yes15no5yes10, data[0], data[1:])
    dataset["id"] = dds.format_dataset_id("yes15no5yes10", str(len(data)))                         
    return convert_pseudo_experimental_to_experimental(dataset)