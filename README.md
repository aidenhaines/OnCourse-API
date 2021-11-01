
  <img width="50px" src="https://cdn.discordapp.com/attachments/848365417688203294/892262456271978566/oncourselogo.svg">

# OnCourse-API

OnCourse-API is a python library meant to make getting data from [OnCourse Connect](https://www.oncourseconnect.com/) a simple task

![PyPI](https://img.shields.io/pypi/v/oncourse-api) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oncourse-api?color=blue)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install oncourse_api
```

## Usage

```python
from oncourse_api.oncourse import OnCourse

data = OnCourse("Username", "Password")

print(data.student) # Prints Student Name

assignments = data.student.getAssignments() # Returns list of assignments

# I love typehinting so your IDE should display options
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
