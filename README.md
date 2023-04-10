# Graphic tool that annotates uploaded images
The main task of Software Engineering course on sixth semester at Silesian University of Technology was to create given application. Our team succesfully delivered web application that lets the user:
- create an account,
- load single or multiple image files,
- annotate image,
- send additional information about camera type or image location,
- save the images in the form of project with customized name in COCO format: .png files with .json, which informs about all made annotations in every included image,
- edit previously annotated image,
- see project statistics about objects frequency.

Main part of application, graphic tool, let the user mark requested object by transparent colorful rectangle. Its color is choosen randomly unless its class label was previously used by the user. 

The technology scope:

- frontend:

  a) HTML,
  
  b) CSS,
  
  c) JavaScript in form of its framework - Vue.js.
  
- backend:

  a) Python in form of its framework - Flask,
  
  b) MySQL database.


The team worked in given squad:

- [jdylik](https://github.com/jdylik) - graphic tool (drawing, editing), JavaScript internal logic, Flask requests, compressing and saving system of application, user inputs processing, statistics,
- [admat00](https://github.com/admat00) - visual part of application - CSS and HTML programming, database project,
- [kaxuu](https://github.com/kaxuu) - compressing and saving system of application, Flask requests,
- [majkel99](https://github.com/majkel99) - logging panel of application, documentation.
