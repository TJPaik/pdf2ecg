import xml.etree.ElementTree as ET

import fitz
import numpy as np

from svgpath2mpl import _parse_path


def parse_path(pathdef, current_pos=0 + 0j):
    verts = []
    for c, v in _parse_path(pathdef, current_pos):
        verts.append(list(v[0]))
    return np.array(verts)


def get_attrib(file_name):
    tree = ET.parse(file_name)
    result = []
    for el in tree.iter():
        if el.tag[-4:] == 'path':
            result.append(el)

    result2 = []
    for el in result:
        result2.append(
            el.attrib['d']
        )
    return result2


def get_attrib_string(str_input):
    tree = ET.fromstring(str_input)
    result = []
    for el in tree.iter():
        if el.tag[-4:] == 'path':
            result.append(el)

    result2 = []
    for el in result:
        result2.append(
            el.attrib['d']
        )
    return result2


def get_svg_data(mode, file_name):
    if mode not in ['H', 'S', 'N1', 'N2', 'N3']:
        raise NotImplementedError('')

    if mode == 'H':
        NUM_BASE = 8
        VALID_LENGTHS = [1247, 1250, 4997]
        FIRST_COLUMN_NUM = 1247
        REMAINED_NUM = 1250
        LAST_NUM = 4997
        DEFAULT_GAP = 82
    elif mode == 'S':
        NUM_BASE = 60
        VALID_LENGTHS = [1238, 5000]
        FIRST_COLUMN_NUM = 1238
        REMAINED_NUM = 1238
        LAST_NUM = 5000
        DEFAULT_GAP = 1000
    elif mode == 'N1':
        NUM_BASE = 60
        VALID_LENGTHS = [619, 2500]
        FIRST_COLUMN_NUM = 619
        REMAINED_NUM = 619
        LAST_NUM = 2500
        DEFAULT_GAP = 1000
    elif mode == 'N2':
        NUM_BASE = 60
        VALID_LENGTHS = [619, 2500]
        FIRST_COLUMN_NUM = 619
        REMAINED_NUM = 619
        LAST_NUM = 2500
        DEFAULT_GAP = 500
    else:
        NUM_BASE = 60
        VALID_LENGTHS = [1238, 5000]
        FIRST_COLUMN_NUM = 1238
        REMAINED_NUM = 1238
        LAST_NUM = 5000
        DEFAULT_GAP = 2001

    def get_base(arrays):
        _result = []
        for _el in arrays:
            if len(_el) == NUM_BASE:
                assert np.max(_el[:, 1]) - _el[0][1] == DEFAULT_GAP
                _result.append(_el[0][1])
        return _result

    def get_data(arrays):
        _result = []
        for _el in arrays:
            if len(_el) in VALID_LENGTHS:
                _result.append(_el)
        return _result

    if file_name[0] == '<':
        attribs = get_attrib_string(file_name)
    else:
        attribs = get_attrib(file_name)

    result = []
    for el in attribs:
        result.append(
            parse_path(el)
        )

    base = get_base(result)
    list_of_arrays = get_data(result)
    assert len(base) == 4
    assert len(list_of_arrays) == 13

    base.sort(reverse=True)
    list_of_arrays.sort(reverse=True, key=lambda x: np.median(x[:, 1]))

    first_row = list_of_arrays[:4]
    second_row = list_of_arrays[4:8]
    third_row = list_of_arrays[8:12]
    last_row = list_of_arrays[-1]
    first_row.sort(key=lambda x: x[0][0])
    second_row.sort(key=lambda x: x[0][0])
    third_row.sort(key=lambda x: x[0][0])

    wave_1 = first_row[0] - np.array([[0, base[0]]] * FIRST_COLUMN_NUM)
    wave_aVR = first_row[1] - np.array([[0, base[0]]] * REMAINED_NUM)
    wave_V1 = first_row[2] - np.array([[0, base[0]]] * REMAINED_NUM)
    wave_V4 = first_row[3] - np.array([[0, base[0]]] * REMAINED_NUM)

    wave_2 = second_row[0] - np.array([[0, base[1]]] * FIRST_COLUMN_NUM)
    wave_aVL = second_row[1] - np.array([[0, base[1]]] * REMAINED_NUM)
    wave_V2 = second_row[2] - np.array([[0, base[1]]] * REMAINED_NUM)
    wave_V5 = second_row[3] - np.array([[0, base[1]]] * REMAINED_NUM)

    wave_3 = third_row[0] - np.array([[0, base[2]]] * FIRST_COLUMN_NUM)
    wave_aVF = third_row[1] - np.array([[0, base[2]]] * REMAINED_NUM)
    wave_V3 = third_row[2] - np.array([[0, base[2]]] * REMAINED_NUM)
    wave_V6 = third_row[3] - np.array([[0, base[2]]] * REMAINED_NUM)

    wave_2_whole = last_row - np.array([[0, base[3]]] * LAST_NUM)

    return [
        wave_2_whole,
        wave_1,
        wave_2,
        wave_3,
        wave_aVR,
        wave_aVL,
        wave_aVF,
        wave_V1,
        wave_V2,
        wave_V3,
        wave_V4,
        wave_V5,
        wave_V6,
    ]


def get_pdf_data(mode, file_name):
    with open(file_name, 'rb') as f:
        tmp = f.read()
    doc = fitz.open(stream=tmp)
    page = doc.load_page(0)
    svg = page.get_svg_image(matrix=fitz.Identity, text_as_path=False)
    return get_svg_data(mode, svg)


if __name__ == '__main__':
    A = get_svg_data('S', '/home/paiktj/abc.svg')
    B = get_pdf_data('S', '/home/paiktj/abc.pdf')
