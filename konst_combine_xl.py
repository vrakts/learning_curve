#import libraries
import pandas as pd
import glob

#import excel files
path = 'YOUR_PATH HERE'
extension = 'xlsx' #grab all excel files
excels = glob.glob('*.{}'.format(extension))