# RayTracer

This is my implementation of a ray tracer created in Python for the final assignment of [CSC 305: Computer Graphics](https://www.uvic.ca/calendar/undergrad/index.php#/courses/H1p5ku6XV "UVic Course Page") at UVic. This program renders a scene from a camera (positioned at origin) given a test file in .txt format which has parameters for the scene, the objects, and the lights. It currently supports ellipsoidal shapes (spheres scaled in x, y or z) by using the sphere quadtratic formula to find intersections. It outputs a rendered image file in color with ambient, diffuse, specular, reflection, and shadows. Multiple objects and multiple lights with varying parameters such as light color intensity are supported.

# Renders

## Intersection

<img src="https://raw.githubusercontent.com/kutaycinar/RayTracer/main/tests/testIntersection.png" width="200" height="200">

## Ambient

<img src="https://raw.githubusercontent.com/kutaycinar/RayTracer/main/tests/testAmbient.png" width="200" height="200">

## Diffuse

<img src="https://raw.githubusercontent.com/kutaycinar/RayTracer/main/tests/testDiffuse.png" width="200" height="200">

## Specular

<img src="https://raw.githubusercontent.com/kutaycinar/RayTracer/main/tests/testSpecular.png" width="200" height="200">

## Reflection

<img src="https://raw.githubusercontent.com/kutaycinar/RayTracer/main/tests/testReflection.png" width="200" height="200">

## Shadow

<img src="https://raw.githubusercontent.com/kutaycinar/RayTracer/main/tests/testShadow.png" width="200" height="200">

## Illumination

<img src="https://raw.githubusercontent.com/kutaycinar/RayTracer/main/tests/testIllum.png" width="200" height="200">
