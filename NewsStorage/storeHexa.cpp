#include <Python.h>
#include <iostream>
#include <string>
#include <fstream>

int getKey(PyObject* pModule, const std::string& imagePath) {
    int key = -1; 

    PyObject* pCreateKey = PyObject_GetAttrString(pModule, "createKey");
    if (pCreateKey && PyCallable_Check(pCreateKey)) {
        PyObject* pArgs = PyTuple_Pack(1, PyUnicode_FromString(imagePath.c_str()));
        PyObject* pKey = PyObject_CallObject(pCreateKey, pArgs);
        Py_DECREF(pArgs);

        if (pKey != nullptr) {
            if (PyLong_Check(pKey)) {
                key = PyLong_AsLong(pKey);
            } else {
                std::cerr << "Error: createKey() did not return an integer." << std::endl;
            }
            Py_DECREF(pKey);
        } else {
            PyErr_Print();
        }
        Py_DECREF(pCreateKey);
    } else {
        std::cerr << "Error: createKey() function not found or not callable." << std::endl;
        PyErr_Print();
    }

    return key;
}

std::string getHexadecimalValue(PyObject* pModule, const std::string& imagePath) {
    std::string hexDecValue = "";

    PyObject* pGetHexadecimal = PyObject_GetAttrString(pModule, "getHexadecimal");
    if (pGetHexadecimal && PyCallable_Check(pGetHexadecimal)) {
        PyObject* pArgs = PyTuple_Pack(1, PyUnicode_FromString(imagePath.c_str()));
        PyObject* pHexDecValue = PyObject_CallObject(pGetHexadecimal, pArgs);
        Py_DECREF(pArgs);

        if (pHexDecValue != nullptr) {
            if (PyUnicode_Check(pHexDecValue)) {
                hexDecValue = PyUnicode_AsUTF8(pHexDecValue);
            } else {
                std::cerr << "Error: getHexadecimal() did not return a string." << std::endl;
            }
            Py_DECREF(pHexDecValue);
        } else {
            PyErr_Print();
        }
        Py_DECREF(pGetHexadecimal);
    } else {
        std::cerr << "Error: getHexadecimal() function not found or not callable." << std::endl;
        PyErr_Print();
    }

    return hexDecValue;
}

void addKeyValue(int key, std::string hexDecValue, std::string storage){
        std::ofstream file(storage, std::ios::app);

        if (file.is_open()){
            file << key << "," << hexDecValue << "\n";
            file.close();
            std::cout << "Data Added Successfully!\n";
        }
}


int main() {
    Py_Initialize();

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('NewsStorage')");

    std::string imagePath = "NewsStorage/image.jpg";

    PyObject* pPythonFile = PyUnicode_DecodeFSDefault("genKeyHexa");
    PyObject* pModule = PyImport_Import(pPythonFile);
    Py_DECREF(pPythonFile);

    if (pModule != nullptr) {
        std::string storage = "NewsStorage/storage.csv";
        int key = getKey(pModule, imagePath);
        std::string hexDecValue = getHexadecimalValue(pModule, imagePath);

        std::cout << "Key: " << key << " Hexadecimal Value: " << hexDecValue << std::endl;
        addKeyValue(key, hexDecValue, storage);

        Py_DECREF(pModule);
    } 
    else {
        std::cerr << "Error: Could not import Python module." << std::endl;
        PyErr_Print();
    }

    Py_Finalize();
    return 0;
}
