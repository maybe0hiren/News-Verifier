#include <Python.h>
#include <iostream>
#include <string>

int main() {
    Py_Initialize();

    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('NewsStorage')");

    std::string imagePath = "NewsStorage/image.jpg";

    PyObject *pPythonFile = PyUnicode_DecodeFSDefault("genKeyHexa");
    PyObject *pModule = PyImport_Import(pPythonFile);
    Py_DECREF(pPythonFile);

    if (pModule != nullptr) {

        PyObject *pCreateKey = PyObject_GetAttrString(pModule, "createKey");
        if (pCreateKey && PyCallable_Check(pCreateKey)) {
            PyObject *pArgs1 = PyTuple_Pack(1, PyUnicode_FromString(imagePath.c_str()));
            PyObject *pKey = PyObject_CallObject(pCreateKey, pArgs1);
            Py_DECREF(pArgs1);

            if (pKey != nullptr) {
                if (PyLong_Check(pKey)) {
                    int key = PyLong_AsLong(pKey);
                    std::cout << "Key: " << key << std::endl;
                } 
                else {
                    std::cerr << "Error: Integer." << std::endl;
                }
                Py_DECREF(pKey);
            } 
            else {
                PyErr_Print();
            }
            Py_DECREF(pCreateKey);
        } 
        else {
            std::cerr << "Error: createKey()" << std::endl;
            PyErr_Print();
        }

        PyObject *pGetHexadecimal = PyObject_GetAttrString(pModule, "getHexadecimal");
        if (pGetHexadecimal && PyCallable_Check(pGetHexadecimal)) {
            PyObject *pArgument2 = PyTuple_Pack(1, PyUnicode_FromString(imagePath.c_str()));
            PyObject *pHexDecValue = PyObject_CallObject(pGetHexadecimal, pArgument2);
            Py_DECREF(pArgument2);

            if (pHexDecValue != nullptr) {
                if (PyUnicode_Check(pHexDecValue)) {
                    std::string hexDecValue = PyUnicode_AsUTF8(pHexDecValue);
                    std::cout << "Returned String: " << hexDecValue << std::endl;
                } 
                else {
                    std::cerr << "Error: getHexadecimal()" << std::endl;
                }
                Py_DECREF(pHexDecValue);
            } 
            else {
                PyErr_Print();
            }
            Py_DECREF(pGetHexadecimal);
        } 
        else {
            std::cerr << "Error: Hexadecimal Value" << std::endl;
            PyErr_Print();
        }

        Py_DECREF(pModule);
    } else {
        std::cerr << "Error: Python Module" << std::endl;
        PyErr_Print();
    }

    Py_Finalize();
    return 0;
}
