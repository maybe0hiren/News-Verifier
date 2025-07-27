#include <Python.h>
#include <sqlite3.h>
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

// void addKeyValue(int key, std::string hexDecValue, std::string storage){
//         std::ofstream file(storage, std::ios::app);

//         if (file.is_open()){
//             file << key << "," << hexDecValue << "\n";
//             file.close();
//             std::cout << "Data Added Successfully!\n";
//         }
// }

void dbInsertPair(int key, const std::string hexaDecValue, const std::string &dbName){
    sqlite3 *db;
    char *err = 0;

    if (sqlite3_open(dbName.c_str(), &db)){
        std::cerr << "Error: Opening Database " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    std::string table = 
        "CREATE TABLE IF NOT EXISTS storage ("
        "key INTEGER, "
        "hexaDecValue TEXT);";
    
    if (sqlite3_exec(db, table.c_str(), 0, 0, &err) != SQLITE_OK){
        std::cerr << "Table Creation Error: " << err << std::endl;
        sqlite3_free(err);
    }

    std::string keyValue = "INSERT INTO storage (key, hexaDecValue) VALUES (" +
                  std::to_string(key) + ", '" + hexaDecValue + "');";
    if (sqlite3_exec(db, keyValue.c_str(), 0, 0, &err) != SQLITE_OK){
        std::cerr << "Inserting Error: " << err << std::endl;
        sqlite3_free(err);
    }
    else{
        std::cout << "Key: " << key << " - Value: " << hexaDecValue << " Inserted!" << std::endl;
    }
    sqlite3_close(db);
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
        std::string hexaDecValue = getHexadecimalValue(pModule, imagePath);
        std::cout << "Key: " << key << " Hexadecimal Value: " << hexaDecValue << std::endl;
        dbInsertPair(key, hexaDecValue, "NewsStorage/storage.db");
        Py_DECREF(pModule);
    } 
    else {
        std::cerr << "Error: Could not import Python module." << std::endl;
        PyErr_Print();
    }

    Py_Finalize();
    return 0;
}
