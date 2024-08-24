# HairArranger
This Belnder add-on is a collection of properties and scripts that helps designers to generate, modify, and set stylized hair.\
**This is under development!!** <br/><br/>
[![](https://img.youtube.com/vi/IdA8vOoua7w/0.jpg)](https://www.youtube.com/watch?v=IdA8vOoua7w)

## Installation
Download and put the 'hair_arranger' folder in your Blender addons folder or use the 'Install from File...' menu on Blender.

## How to use
### Start
Select target mesh on 3D view in Object mode and click the "Start" button in Hair Arranger Tab > Hair Arranger.\
\
<img src="https://user-images.githubusercontent.com/47211856/175775154-e18c63bd-ecb6-4573-9499-a1036bc96621.png" width="215">

### Menu
![image](https://github.com/user-attachments/assets/cb4a686d-1a61-4d64-a0e7-d72f424e456d)
\
You can see the detail of each property in Blender documentation, [Draw](https://docs.blender.org/manual/en/4.2/modeling/curves/tools/draw.html) or [Geometry](https://docs.blender.org/manual/en/4.2/modeling/curves/properties/geometry.html).
#### General settings for modeling
* **Use Snap**: Snap on/off
* **Snap Only First**: Only uses the start of the stroke for the depth.
* **Surface**: The orientation plane to draw on.

- **Normal Visibility**: Normal visibility on/off
- **Normal Display Length**:length for normal display

#### Properties for curve Draw tool
* **Tolerance**: Lower values give a result that is closer to the drawing stroke, while higher values give more smoothed results.
* **offset**: Distance to offset the curve from the surface.
* **Taper Start**: Tapering level at start point.
* **Taper End**: Tapering level at end point.

#### Properties for generated curves
* **Radius**: The width of the extrusion along the curve. This can also be used to adjust the display size of the curve while drawing.
* **Resolution U**: The number of points that are computed between every pair of control points. Curves can be made more smooth by increasing the resolution respectively.
* **Bevel Start**: Defines the starting point of the bevel geometry on the curve. 
* **Bevel End**: Defines the ending point of the bevel geometry on the curve.
* **Object**: A curve object which will be extruded along the curve. Four curves are provided in advance, and users can also add new curves.

#### Edit object to extrude
* **ScaleX**, **ScaleY**: Scale the haircurve objects

#### Selecting
* **Select Spline**: Click with one point of the curve selected to select all points of the spline.
* **Select All Spline**: Select all points of all curves of the current curve object.
* **Select Starts**: Select all start points of all curves in the current curve object.
* **Select Middle**: Selects all midpoints, excluding the start and end points, of all curves in the current curve object.
* **Select Ends**: Select all end points of all curves in the current curve object.

#### Conversion and Utils
* **Convert to NURBS**: Convert selected BezierCurve into NURBS curve
* **Remoce End Points**: Remove both end points of the selected NURBS curve. This can be used for removing unused end points after converting to NURBS curve.
* **Spearate Curve**s: Separate all curves into each single curve objects. This can be used for reconstruct the hair object into small objects.
* **Convert to Mesh**: Convert all curves into mesh object. The resolution depends on the curve resolution.

### How to add custom haircurve
Open hair_arranger/hair_curves.blend and add your custom curve with the name which **starts from "haircurve_"**. \
![image](https://github.com/user-attachments/assets/8307c12c-a582-4af7-8794-4e43393a43ea)
\
Then the curve will be automatically loaded into the haircurves locator and can be selected on the UI.\
![image](https://github.com/user-attachments/assets/7c29df93-ed2f-4124-b25d-1e4f532a11f3)

## Caution
This is under development and it may contain some critical bugs. \
Please note that we will not be liable for any damages caused by use of this add-on and scripts.

