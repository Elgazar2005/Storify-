import os
from core.file_singletone import FileSingleton

def test_file_singleton():
    f1=FileSingleton()
    f2=FileSingleton()
    assert f1 is f2

def test_read_and_write_csv(tmp_path):
    file=FileSingleton()
    testfile=tmp_path/"test.csv"
    fieldnames=["id","name"]
    rows = [
    {"id": "1", "name": "Ahmed"},
    {"id": "2", "name": "Samaa"},
    {"id": "3", "name": "Omar"}
]
    file.write_csv(str(testfile),fieldnames,rows)
    result=file.read_csv(str(testfile))
    assert len(result)==3
    assert result[1]["name"]=="Samaa"
    assert result[1]["id"]=="2"

def test_append_csv(tmp_path):
    file=FileSingleton()
    testfile=tmp_path/"test.csv"
    fieldnames = ["id", "value"]
    file.append_csv(str(testfile), fieldnames, {"id": "1", "value": "A"})
    file.append_csv(str(testfile), fieldnames, {"id": "2", "value": "B"})
    result=file.read_csv(str(testfile))
    assert len(result)==2
    assert len(result) == 2
    assert result[1]["value"] == "B"