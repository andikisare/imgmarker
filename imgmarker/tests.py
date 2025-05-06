import sys
import os
import pytest
from pytestqt.qtbot import QtBot
import numpy as np
from getpass import getuser
import datetime as dt
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser('~')
def _resource_path(rel_path):
    if hasattr(sys,'_MEIPASS'): 
        base_path = sys._MEIPASS
    else: base_path = MODULE_PATH
    return os.path.join(base_path, rel_path)

if __name__ == '__main__' and __package__ is None:
    top = os.path.abspath(os.path.join(MODULE_PATH, '..'))
    sys.path.append(str(top))
        
    import imgmarker
    __package__ = 'imgmarker'

ICON = _resource_path('icon.ico')
HEART_SOLID = _resource_path('heart_solid.ico')
HEART_CLEAR = _resource_path('heart_clear.ico')
from .gui.window import MainWindow
from . import gui, config, io, image

test_save_dir = "./tests/test_save/"
test_images_dir = "./tests/test_images/"
test_catalog_dir_txt = "./tests/TEST_catalog.txt"
test_catalog_dir_csv = "./tests/TEST_catalog.csv"

USER = getuser()

if os.path.exists(test_save_dir):
    os.remove(test_save_dir + f"{USER}_config.txt")
    os.remove(test_save_dir + f"{USER}_marks.csv")
    os.remove(test_save_dir + f"{USER}_images.csv")
    os.rmdir(test_save_dir)
    os.mkdir(test_save_dir)
else:
    os.mkdir(test_save_dir)

@pytest.fixture
def app(qtbot:QtBot):
    config.SAVE_DIR = test_save_dir
    config.IMAGE_DIR = test_images_dir
    config.USER = USER
    test_app = MainWindow()
    qtbot.addWidget(test_app)
    return test_app

def test_load_images(app:MainWindow, qtbot:QtBot):

    assert len(app.images) == 3

def test_image_shown(app:MainWindow, qtbot:QtBot):
    test_load_images(app, qtbot)
    image = app.image_scene.image
    assert image in app.image_scene.items()

def test_import_markfile(app:MainWindow, qtbot:QtBot):
    app.import_markfile(src=test_catalog_dir_csv)

    assert len(io.markpaths()) == 2
    assert len(app.image_scene.items()) == 3

def test_place_mark(app:MainWindow, qtbot):
    for mark in app.image.marks:
        app.image_scene.rmmark(mark)
    for mark in app.imageless_marks:
        app.imageless_marks.remove(mark)
        try: app.image_scene.rmmark(mark)
        except: pass
        
    app.mark(group=1, test=True)

    assert len(app.image_scene.items()) == 3
    assert len(app.image.marks) == 1

def test_mark_limit(app:MainWindow, qtbot:QtBot):
    for mark in app.image.marks:
        app.image_scene.rmmark(mark)
    for mark in app.imageless_marks:
        app.imageless_marks.remove(mark)
        try: app.image_scene.rmmark(mark)
        except: pass

    config.GROUP_MAX[0] = 1
    config.GROUP_MAX[1] = 2

    app.mark(group=1, test=True)
    app.mark(group=1, test=True)
    app.mark(group=2, test=True)
    app.mark(group=2, test=True)
    app.mark(group=2, test=True)

    assert len(app.image_scene.items()) == 7
    assert len(app.image.marks) == 3

def test_mark_delete(app:MainWindow, qtbot:QtBot):
    for mark in app.image.marks:
        app.image_scene.rmmark(mark)
    for mark in app.imageless_marks:
        app.imageless_marks.remove(mark)
        try: app.image_scene.rmmark(mark)
        except: pass

    app.mark(group=1, test=True)
    app.mark(group=2, test=True)
    app.mark(group=3, test=True)
    app.del_usermarks(mode='all')

    assert len(app.image_scene.items()) == 1
    assert len(app.image.marks) == 0

def test_catalog_delete(app:MainWindow, qtbot:QtBot):
    for mark in app.image.marks:
        app.image_scene.rmmark(mark)
    for mark in app.imageless_marks:
        app.imageless_marks.remove(mark)
        try: app.image_scene.rmmark(mark)
        except: pass

    app.import_markfile(src=test_catalog_dir_txt)
    
    assert len(app.image_scene.items()) == 3

    app.shift(+1)
    for mark in app.image.marks:
        app.image_scene.rmmark(mark)

    assert len(app.image_scene.items()) == 3
    
    app.shift(+1)
    for mark in app.image.marks:
        app.image_scene.rmmark(mark)

    assert len(app.image_scene.items()) == 3

    app.del_markfile(os.path.join(config.SAVE_DIR,'imports',test_catalog_dir_txt.split(os.sep)[-1]))

    assert len(app.image_scene.items()) == 1

    app.shift(+1)

    assert len(app.image_scene.items()) == 1

    app.shift(+1)

    assert len(app.image_scene.items()) == 1

def test_frame_seek(app:MainWindow, qtbot:QtBot):
    first_frame_array = app.image.array
    app.image.seek(1)
    second_frame_array = app.image.array

    assert not np.all(first_frame_array == second_frame_array)

def test_save_mark(app:MainWindow, qtbot:QtBot):
    app.mark(group=1, test=True)
    date = 0
    name = 0
    group = 0
    label = 0
    x = 0
    y = 0
    ra = 0
    dec = 0
    line0 = True
    for line in open(os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')):
        if line0: line0 = False
        else:
            date,name,group,label,x,y,ra,dec = [i.strip() for i in line.replace('\n','').split(',')]

    assert date == dt.datetime.now(dt.timezone.utc).date().isoformat()
    assert name == app.image.name
    assert group == config.GROUP_NAMES[1]
    assert label == "None"
    assert x == str(float(app.image.width/2))
    assert y == str(float(app.image.height/2))
    assert ra == str(app.image.marks[0].wcs_center[0])
    assert dec == str(app.image.marks[0].wcs_center[1])

def test_delete_save_mark(app:MainWindow, qtbot:QtBot):
    app.mark(group=1, test=True)
    date = 0
    name = 0
    group = 0
    label = 0
    x = 0
    y = 0
    ra = 0
    dec = 0
    line0 = True
    for line in open(os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')):
        if line0: line0 = False
        else:
            date,name,group,label,x,y,ra,dec = [i.strip() for i in line.replace('\n','').split(',')]

    assert date == dt.datetime.now(dt.timezone.utc).date().isoformat()
    assert name == app.image.name
    assert group == config.GROUP_NAMES[1]
    assert label == "None"
    assert x == str(float(app.image.width/2))
    assert y == str(float(app.image.height/2))
    assert ra == str(app.image.marks[0].wcs_center[0])
    assert dec == str(app.image.marks[0].wcs_center[1])

    app.del_usermarks(mode='all')
    line0 = True
    for line in open(os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')):
        if line0: line0 = False
        else:
            date,name,group,label,x,y,ra,dec = [i.strip() for i in line.replace('\n','').split(',')]

    assert date == dt.datetime.now(dt.timezone.utc).date().isoformat()
    assert name == app.image.name
    assert group == "None"
    assert label == "None"
    assert x == "nan"
    assert y == "nan"
    assert ra == "nan"
    assert dec == "nan"

def test_change_mark_group_save(app:MainWindow, qtbot:QtBot):
    app.mark(group=1, test=True)
    date = 0
    name = 0
    group = 0
    label = 0
    x = 0
    y = 0
    ra = 0
    dec = 0
    line0 = True
    for line in open(os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')):
        if line0: line0 = False
        else:
            date,name,group,label,x,y,ra,dec = [i.strip() for i in line.replace('\n','').split(',')]

    assert date == dt.datetime.now(dt.timezone.utc).date().isoformat()
    assert name == app.image.name
    assert group == config.GROUP_NAMES[1]
    assert label == "None"
    assert x == str(float(app.image.width/2))
    assert y == str(float(app.image.height/2))
    assert ra == str(app.image.marks[0].wcs_center[0])
    assert dec == str(app.image.marks[0].wcs_center[1])

    new_group = "BCG"

    config.GROUP_NAMES[1] = new_group
    app.settings_window.group_boxes[0].setText(new_group)
    app.settings_window.update_config()
    app.save()

    line0 = True
    for line in open(os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')):
        if line0: line0 = False
        else:
            date,name,group,label,x,y,ra,dec = [i.strip() for i in line.replace('\n','').split(',')]
    
    assert date == dt.datetime.now(dt.timezone.utc).date().isoformat()
    assert name == app.image.name
    assert group == new_group
    assert label == "1"
    assert x == str(float(app.image.width/2))
    assert y == str(float(app.image.height/2))
    assert ra == str(app.image.marks[0].wcs_center[0])
    assert dec == str(app.image.marks[0].wcs_center[1])

def test_next_image(app:MainWindow, qtbot):
    current_image_array = app.image.array
    app.shift(+1)
    new_image_array = app.image.array

    assert not np.all(current_image_array == new_image_array)

# def test_save_category(app, qtbot):
#     app.mark(group=1, test=True)
#     date = 0
#     name = 0
#     group = 0
#     label = 0
#     x = 0
#     y = 0
#     ra = 0
#     dec = 0
#     line0 = True
#     for line in open(os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')):
#         if line0: line0 = False
#         else:
#             date,name,group,label,x,y,ra,dec = [i.strip() for i in line.replace('\n','').split(',')]

#     assert date == dt.datetime.now(dt.timezone.utc).date().isoformat()
#     assert name == app.image.name
#     assert group == config.GROUP_NAMES[1]
#     assert label == "None"
#     assert x == str(float(app.image.width/2))
#     assert y == str(float(app.image.height/2))
#     assert ra == str(app.image.marks[0].wcs_center[0]")
#     assert dec == str(app.image.marks[0].wcs_center[1]")