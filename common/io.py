
import pandas as pd


def read_from_csv(filepathname):
    '''
    return          numpy.array
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_read_from_csv.csv"
    '''
    df = pd.read_csv(filepathname, header=1, skipfooter=1)
    data = df.as_matrix()
    return data

def read_from_headless_dataframe(filepathname):
    '''
    return          numpy.array
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_read_from_csv.csv"
    '''
    df = pd.read_csv(filepathname, header=None, index_col=0)
    data = df.as_matrix()
    return data

def write_to_csv(data, filepathname):
    '''
    Overwrites
    data            numpy.array
    filepathnmae    string, e.g., "C:/workspace/resproj/test/common/test_write_to_csv.csv"
    '''
    assert(filepathname is not None)
    if data is None:
        with open(filepathname, 'w') as f:
            f.write("")
            return
    df = pd.DataFrame(data)
    with open(filepathname, 'w') as f:
        #f.write("----------\n")
        df.to_csv(f, header=False)
        #f.write("----------\n")
        
def write_as_dataframe_to_csv(data, filepathname):
    write_to_csv(data, filepathname)
    
    
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


class ResourceLocator():
    
    url = None
    read = False
    write = False

    def set_read(self, flag):
        self.read = flag
        return self
    
    def set_write(self, flag):
        self.write = flag
        return self
    
    def set_url(self, value):
        self.url = value
        return self

   
class FileResources():
    
    predicted_calib = None
    predicted_valid = None
    measured_calib = None
    measured_valid = None
    error_calib = None
    error_valid = None
    multiple_realisations = None
    
    def set_predicted_calibration(self, locator):
        self.predicted_calib = locator
        return self
    
    def set_predicted_validation(self, locator):
        self.predicted_valid = locator
        return self
    
    def set_measured_calibration(self, locator):
        self.measured_calib = locator
        return self

    def set_measured_validation(self, locator):
        self.measured_valid = locator
        return self

    def set_error_calibration(self, locator):
        self.error_calib = locator
        return self

    def set_error_validation(self, locator):
        self.error_valid = locator
        return self
    
    def set_multiple_realisations(self, locator):
        self.multiple_realisations = locator
        return self

    def get_predicted_calibration(self):
        return self.predicted_calib
    
    def get_predicted_validation(self):
        return self.predicted_valid

    def get_measured_calibration(self):
        return self.measured_calib
    
    def get_measured_validation(self):
        return self.measured_valid

    def get_error_calibration(self):
        return self.error_calib
    
    def get_error_validation(self):
        return self.error_valid

    def get_multiple_realisations(self):
        return self.multiple_realisations
