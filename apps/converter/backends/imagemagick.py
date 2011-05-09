import subprocess

from converter.conf.settings import IM_IDENTIFY_PATH
from converter.conf.settings import IM_CONVERT_PATH
from converter.api import QUALITY_DEFAULT, QUALITY_SETTINGS
from converter.exceptions import ConvertError, UnknownFormat, \
    IdentifyError

CONVERTER_ERROR_STRING_NO_DECODER = u'no decode delegate for this image format'


def execute_identify(input_filepath, arguments=None):
    command = []
    command.append(unicode(IM_IDENTIFY_PATH))
    if arguments:
        command.extend(arguments)
    command.append(unicode(input_filepath))

    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        raise IdentifyError(proc.stderr.readline())
    return proc.stdout.read()


def execute_convert(input_filepath, output_filepath, quality=QUALITY_DEFAULT, arguments=None):
    command = []
    command.append(unicode(IM_CONVERT_PATH))
    command.extend(unicode(QUALITY_SETTINGS[quality]).split())
    command.append(unicode(input_filepath))
    if arguments:
        command.extend(unicode(arguments).split())
    command.append(unicode(output_filepath))
    proc = subprocess.Popen(command, close_fds=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    return_code = proc.wait()
    if return_code != 0:
        #Got an error from convert program
        error_line = proc.stderr.readline()
        if CONVERTER_ERROR_STRING_NO_DECODER in error_line:
            #Try to determine from error message which class of error is it
            raise UnknownFormat
        else:
            raise ConvertError(error_line)