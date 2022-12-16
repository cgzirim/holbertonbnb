<h1 align="center">Holbertonbnb</h1>

![hbnb-logo](https://user-images.githubusercontent.com/88312276/196296347-78436f29-0f78-436c-8d93-3c1274eea30e.png)

## About

[Holbertonbnb](https://www.miniairbnb.gq) is a full-stack web application that replicates the search and filter features of Airbnb. It incorporates a dynamic HTML5/CSS3/jQuery front-end with a MySQL database and Flask RESTful API.  
It runs on three Amazon EC2 instances (1 load balancer, 2 applications servers with a replication/master database setup) It utilizes NGINX as a web server, 
HAProxy for loadbalancing, and gunicorn as the application server.

![Screenshot from 2022-12-16 06-22-00](https://user-images.githubusercontent.com/88312276/208028429-bff90aba-67cf-4822-96d4-f35b25aaabea.png)


As a first-year project at ALX, Holbertonbnb was developed over the course of two months and four versions, which are listed below:
1. [AirBnB clone](https://github.com/iChigozirim/AirBnB_clone)
2. [AirBnB clone v2](https://github.com/iChigozirim/AirBnB_clone_v2)
3. [AirBnB clone v3](https://github.com/dnjoe96/AirBnB_clone_v3)
4. [AirBnB clone v4](https://github.com/iChigozirim/AirBnB_clone_v4) 

The project involved working with pre-existing codebases and collaborating with different cohort mates on each iteration.

This repository is a duplicate of [AirBnB_clone_v4](https://github.com/iChigozirim/AirBnB_clone_v4). However, I have streamlined and organized it, removing extraneous code and improving the front-end. In addition, I created a new Fabric script to automate 90% of the program's deployment, and implemented a new feature - [the web console](https://www.miniairbnb.gq/#console).


### This repository contains the following:

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
  - [Source code](./fabfile.py)
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

Comprehensive documentation to assist with understanding and using the application can be found [here](./documentation)

## Author :black_nib:

- **Chigozirim Igweamaka** - <[iChigozirim](https://github.com/iChigozirim)>

## License :lock:

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details
