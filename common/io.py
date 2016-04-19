
import pandas as pd


def read_from_csv(filepathname):
    '''
    return          numpy.array
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_read_from_csv.csv"
    '''
    #df = pd.read_csv(filepathname, header=1, skipfooter=1)
    df = pd.read_csv(filepathname, header=None, index_col=0)
    data = df.as_matrix()
    return data


def write_to_csv(data, filepathname):
    '''
    Overwrites
    data            numpy.array
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_write_to_csv.csv"
    '''
    df = pd.DataFrame(data)
    with open(filepathname, 'w') as f:
        #f.write("----------\n")
        df.to_csv(f, header=False)
        #f.write("----------\n")
        

def write_to_csv_append(data, filepathname):
    '''
    Appends
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
    Overwrites
    data            string
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_write_to_txt.txt"
    '''
    with open(filepathname, 'w') as f:
        #f.write("----------\n")
        f.writelines(data+"\n")
        #f.write("----------\n")
        
        
def write_to_txt_append(data, filepathname):
    '''
    Appends
    data            string
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_write_to_txt.txt"
    '''
    with open(filepathname, 'a') as f:
        f.write("----------\n")
        f.writelines(data+"\n")
        f.write("----------\n")


def delete_file(filename):
    with open(filename, "w"):
        pass
    
    
def open_file(filename, notfoundisfatal):
    notfoundisnotfata = not notfoundisfatal
    assert(notfoundisnotfata)
    ff = open(filename, 'a')
    return ff