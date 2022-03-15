from werkzeug.utils import secure_filename
import os
import ntpath
from pathlib import Path

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
ALLOWED_EXTENSIONS = {'csv', 'json', 'sql', 'xml'}
UPLOAD_FOLDER = PROJECT_ROOT + '/data'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class FileUpload():

    """
    place all methods needed to upload and read data
    """

    # upload a validated file
    def dump_file(file):

        # check if filename is present
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return file.filename

    # read a known file
    def read_file(filename):
        
        data_folder = Path(PROJECT_ROOT + '/data')
        file_to_open = data_folder / filename

        f = open(file_to_open)

        # return filename and the opened file
        filename_extension = ntpath.basename(file_to_open).split(".")[1]

        data = {
            "filename": ntpath.basename(file_to_open),
            "filename_extension": filename_extension,
            "file": f 
        }
        return data