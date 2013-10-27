import sublime
import platform
import os
import subprocess
import re


class Hugs:
    """
    Responsible for handling hugs instance on the system
    """

    hugs_root = ""
    hugs_root_win = "C:\Program Files (x86)\WinHugs"

    # platform
    current_system = ""

    # tools
    runhugs = "runhugs"
    hugs = "hugs"

    # response regular expressions

    def __init__(self):
        """
        Initialises hugs_root
        """

        # get current os
        self.current_system = platform.system()

        # first, check settings
        settings = sublime.load_settings("Kisses.sublime-settings")
        hugs_setting = sublime.active_window().active_view().settings().get("hugs_root")
        if hugs_setting is None:
            # try to guess
            if self.current_system == "Windows":
                # c:\program files (x86)\WinHugs\
                if os.path.exists(self.hugs_root_win):
                    self.hugs_root = self.hugs_root_win
                    self.checkModules()
                else:
                    raise Exception("Cannot found Hugs98 installation. \n" +
                                    "Please use 'hugs_root' setting to set Hugs directory.")
            else:
                raise Exception("Linux is not yet supported")
                # TODO: run "whereis hugs" or something like that
        else:
            self.hugs_root = hugs_setting
            self.checkModules()

    def checkModules(self):
        """
        Checks if everything present : runhugs and hugs
        If not, throws exception
        """
        if self.current_system == "Windows":
            self.runhugs += ".exe"
            self.hugs += ".exe"

        self.runhugs = self.hugs_root + os.sep + self.runhugs
        self.hugs = self.hugs_root + os.sep + self.hugs

        if not os.path.exists(self.hugs) or not os.path.exists(self.runhugs):
            raise Exception("Cannot find " + self.hugs + " or " + self.runhugs +
                            " Check if your installation is corrupt.")
        print("Found Hugs at: " + self.hugs)
        print("Found runhugs at: " + self.runhugs)

    def runHugs(self, sourceFile, commandLine):
        """
        Run hugs and load specified sourceFile
        """
        # run subprocess
        kwargs = {}
        if subprocess.mswindows:
            su = subprocess.STARTUPINFO()
            su.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            su.wShowWindow = subprocess.SW_HIDE
            kwargs['startupinfo'] = su
            proc = subprocess.Popen([self.hugs, "-i +T -98", sourceFile], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                startupinfo=su)
        else:
            proc = subprocess.Popen([self.hugs, "-i +T -98", sourceFile], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        (so, se) = proc.communicate(input=commandLine.encode("utf-8"))
        return str(so)

    def processResponse(self, output, parser):
        """
        Parses results of runHugs(...)
        """
        results = []
        lines = output.split('\\r\\n')
        for line in lines:
            # strip prompt
            buf = line
            try:
                pos = buf.index('>')
                buf = buf[pos + 1:]
            except ValueError:
                pass
            buf = buf.strip()
            # feed appropriate parser
            result = parser.run(buf)
            if result is not None:
                results.append(result)
        return results


class HugsMessage:
    """
    Encapsulates certain Hugs response
    """
    message = ''

    def __init__(self, message):
        self.message = message


class HugsError:
    """
    A placeholder for error information
    """
    lineNo = -1
    sourceFile = ""

    def __init__(self, message, sourceFile="", lineNo=-1):
        """
        Initialises instance
        """
        HugsMessage.__init__(self, message)
        self.lineNo = lineNo
        self.sourceFile = sourceFile


class BaseParser:
    """
    Base class for parsing Hugs response
    """
    errorPattern = re.compile('\AERROR\s-\s(.+)')
    sourceErrorPattern = re.compile('ERROR\s+(".+"):(\d+)\s+-\s+(.+)')

    def run(self, buf):
        """
        Checks input against common regexp, returns HugsError or None
        if string does not match
        """
        src_match = self.sourceErrorPattern.match(buf)
        if src_match:
            return HugsError(src_match.groups(0)[2], src_match.groups(0)[0], src_match.groups(0)[1])
        error_match = self.errorPattern.match(buf)
        if error_match:
            return HugsError(error_match.groups(0)[0])
        return None


class TypeParser(BaseParser):

    expression = ''

    def __init__(self, expression):
        self.expression = expression

    def run(self, buf):
        """
        Check if given string contains an expression which type we requesting
        """
        error = BaseParser.run(self, buf)
        if error is not None:
            return error
        if buf.startswith(self.expression):
            return HugsMessage(buf)
        return None
