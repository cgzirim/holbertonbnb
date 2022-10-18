<h1 align="center">Holbertonbnb</h1>
<p align="center">An Airbnb clone.</p>

![hbnb-logo](https://user-images.githubusercontent.com/88312276/196296347-78436f29-0f78-436c-8d93-3c1274eea30e.png)

## Description

Holbertonbnb is a full-stack web application that replicates the search and filter features of Airbnb. It incorporates a dynamic HTML5/CSS3/jQuery front-end with a MySQL database and Flask RESTful API.

![hbnb-stack](https://user-images.githubusercontent.com/88312276/196298024-9488b0b2-c11d-4254-8cbe-41f20a1ed82e.png)

Holberton School's first-year curriculum used Holbertonbnb as its central web application. The project took two months and four versions. You can see each of the project's four iterations at the links below:

1. [AirBnB clone](https://github.com/iChigozirim/AirBnB_clone)
2. [AirBnB clone v2](https://github.com/iChigozirim/AirBnB_clone_v2)
3. [AirBnB clone v3](https://github.com/dnjoe96/AirBnB_clone_v3)
4. [AirBnB clone v4](https://github.com/iChigozirim/AirBnB_clone_v4)  

The aforementioned versions are segregated, independent codebases. Versions 2, 3, and 4 all inherited and built on repositories created by earlier Holberton School cohorts, unlike the first, which was entirely new. Additionally, I collaborated and pair programmed with a cohort mate for each version of the work produced. I worked with a different cohort mate for each version.

Working with unfamiliar, developed codebases and pair programming were both much enhanced by this versioning process. The lack of a central, well-organized repository where I could showcase all the work I coded and learnt throughout this clone, however, made it less than ideal from the perspective of my portfolio.

Just the above—a streamlined, organized version of Holbertonbnb—is contained in this repository. If you must, call it a minified build.

I started this repository as a duplicate of [AirBnB_clone_v4](https://github.com/iChigozirim/AirBnB_clone_v4), the final version worked on within the scope of Holberton's curriculum. Since then, I have:

- Organized only the code required to deploy the program, cutting out all unnecessary code.
- improved the front-end and created new Fabric for auto-deployment.
- Wrote thorough, organized documentation for all parts of repo.
- Implemented a new feature - the web_terminal.

### What this repository does include:

- Models class system built in Python.

  - [Source code](./models)
  - [Documentation](./documentation/MODELS.md)

- Python console to manage back-end models

  - [Source code](./console.py)
  - [Documentation](./documentation/CONSOLE.md)

- Flask web application server rendering HTML templates with Jinja2

  - [Source code](./web_flask)
  - [Documentation](./documentation/WEB_FLASK.md)

- RESTful Flask API

  - [Source code](./api)
  - [Documentation](./documentation/API.md)
  - Swagger documentation - [miniairbnb.gq/apidocs](https://miniairbnb.gq/apidocs)

- Automatic deployment script.
  - [fabfile.py](./fabfile.py)
  - [Documentation](./documentation/DEPLOYMENT.md)

- Test suit

  - [Source code](./tests)
  - [Documentation](./documentation/TESTS.md)

## Dependencies :couple:

Application:

| Tool/Library  | Version |
| ------------  | ------- |
| Python        | ^3.6.4  |
| MySQL         | ^5.6.0  |
| Flask         | ^1.0.3  |
| flasgger      | ^0.9.2  |
| Flask-Cors    | ^3.0.8  |
| Flask-socketio| ^5.0.0  |
| mysqlclient   | ^1.3.10 |
| SQLAlchemy    | ^1.3.5  |

View the complete list of app dependencies in the [requirements.txt](./requirements.txt).

Deployment:

| Tool/Library | Version |
| ------------ | ------- |
| Python       | ^3.7.3  |
| gunicorn     | ^19.9.0 |
| Fabric       | ^2.4.0  |

## Documentation :book:

In case you missed it - I've documented this entire repository! [Please do check it out!](./documentation)

## Author :black_nib:

- **Chigozirim Igweamaka** - <[iChigozirim](https://github.com/iChigozirim)>

## License :lock:

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details
