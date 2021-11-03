import logging
from json import loads
from re import MULTILINE, search

import requests

from oncourse_api.errors import InvalidCredentials, InvalidPassword, LockedOut

from .models.active_profile import ActiveProfile


logger_name = "oncourse_api"

log = logging.getLogger(logger_name)


class OnCourse:
    def __init__(self, username: str, password: str):
        # Start requests session
        self.requestSession = requests.Session()
        """ Start the request session """

        # Login Info
        self.__username: str = username
        """ Login Username """
        self.__password = password
        """ Login Password """
        self.cookie: str = self.__getCookie()
        """ Returns OnCourse auth cookie """

    def __getCookie(self) -> bool:
        url = "https://www.oncourseconnect.com/account/login"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"Username": self.__username, "Password": self.__password}
        resp = self.requestSession.post(url, headers=headers, data=data)

        # Check for invalid credentials

        if "Invalid username or password." in resp.text:  # Incorrect username
            raise InvalidCredentials(f"No user '{self.__username}' was found.")

        elif "Username or password was invalid." in resp.text:  # Incorrect password
            locked_out = r"(\d+) attempts remaining before your account will be temporarily locked out for (\d+)"
            locked_out = search(locked_out, resp.text, MULTILINE)
            if locked_out.group(1) and locked_out.group(2):
                raise InvalidPassword(f"Password incorrect. {locked_out.group()} minute(s)")

        elif "Due to numerous incorrect attempts" in resp.text:  # Locked out
            duration = r"temporarily locked out for (\d+)"
            duration = search(duration, resp.text, MULTILINE)
            raise LockedOut(
                f"The account has been locked out for {duration.group(1)} minute(s). Too many invalid login attempts"
            )

        # -------------------------------------

        oncourse_cookie = self.requestSession.cookies.get("_occauth")
        self.requestSession.headers.update({"Cookie": f"_occauth={oncourse_cookie}"})
        return oncourse_cookie

    @property
    def active_profile(self) -> ActiveProfile:
        """Request active profile

        returns:
            'ActiveProfile'
        """
        url = "https://www.oncourseconnect.com/#/studentdata"
        source = (self.requestSession.get(url)).text
        regex = r"window.activeProfile = {(.*)}"
        windowActiveProfile = search(regex, source, MULTILINE)
        active_profile = loads("{" + windowActiveProfile.group(1) + "}")
        log.info(f"Logged in as: {active_profile.get('fullName')}")
        return ActiveProfile(active_profile, self.requestSession)
