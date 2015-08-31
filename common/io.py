
import pandas as pd


def read_from_csv(filepathname):
    '''
    return          numpy.array
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_read_from_csv.csv"
    '''
    df = pd.read_csv(filepathname, header=1, skipfooter=1)
    data = df.as_matrix()
    return data


def write_to_csv(data, filepathname):
    '''
    data            numpy.array
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_write_to_csv.csv"
    '''
    df = pd.DataFrame(data)
    with open(filepathname, 'a') as f:
        f.write("----------\n")
        df.to_csv(f, header=False)
        f.write("----------\n")
        

def write_to_txt(data, filepathname):
    '''
    data            string
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_write_to_txt.txt"
    '''
    with open(filepathname, 'a') as f:
        f.write("----------\n")
        f.writelines(data+"\n")
        f.write("----------\n")