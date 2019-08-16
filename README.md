# Road_Labeler
Lane, Road Mark, Traffic Sign, Vanishing Point Labeling Tools
![DEMO2](/image/demo2.png)

## Features
* Support lane, road mark, traffic sign, vanishing point labeling tools
* Multiple vertices line & polygon support
* Draggable Points
* Variable image size support (all images must be the same size)
* Support window resizing

## Dependency
* Python 3
* PyQt5
* Matplotlib
* Pillow

## Labeling Process
### Data Preparation
Put the data to be used for labeling in the `data` folder. When executing the program, it automatically creates a list of files in `data` folder and proceeds labeling.
```
Road_Labeler_Path
├── main.py
├── marker.py
├── ui.py
├── updater.py
├── postprocess.py
└── data
    ├── video01
    │   ├── frame0001.jpg
    │   ├── frame0002.jpg
    │   ├── frame0003.jpg
    │   └── ...
    ├── video02
    ├── video03
    └── ...
```

### Data Labeling
Run `main.py` to execute the program. A single executable file created using pyexe can be downloaded here.

### Data Postprocessing
Run `postprocess.py` to generate labeled image.

## Demo Images
| ![DEMO1](/image/demo1.png) | ![DEMO4](/image/demo4.png) |
|:--------:|:--------:|
| ![DEMO3](/image/demo3.png) | ![DEMO5](/image/demo5.png) |


