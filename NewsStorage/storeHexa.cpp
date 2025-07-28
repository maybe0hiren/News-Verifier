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


void dbInsertPair(int key, const std::string hexaDecValue, const std::string &dbName){
    sqlite3 *db;
    char *err = 0;

    if (sqlite3_open(dbName.c_str(), &db)){
        std::cerr << "Error: Opening Database " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    std::string tableQuery = 
        "CREATE TABLE IF NOT EXISTS storage ("
        "key INTEGER, "
        "hexaDecValue TEXT);";
    
    if (sqlite3_exec(db, tableQuery.c_str(), 0, 0, &err) != SQLITE_OK){
        std::cerr << "Table Creation Error: " << err << std::endl;
        sqlite3_free(err);
    }

    std::string insertQuery = "INSERT INTO storage (key, hexaDecValue1) VALUES (" +
                  std::to_string(key) + ", '" + hexaDecValue + "');";
    if (sqlite3_exec(db, insertQuery.c_str(), 0, 0, &err) != SQLITE_OK){
        std::cerr << "Inserting Error: " << err << std::endl;
        sqlite3_free(err);
    }
    else{
        std::cout << "Key: " << key << " - Value: " << hexaDecValue << " Inserted!" << std::endl;
    }
    sqlite3_close(db);
}

void dbAppendPair(int key, const std::string &hexaDecValue, const std::string &dbName){
    sqlite3 *db;
    int opCheck = sqlite3_open(dbName.c_str(), &db);

    if (opCheck != SQLITE_OK){
        std::cerr << "Error Opening the Database: " << sqlite3_errmsg(db) << std::endl;
        return;
    }

    std::string selectQuery = "SELECT ";
    for (int i = 2; i <= 50; ++i){
        selectQuery += "hexaDecValue" + std::to_string(i);
        if (i < 50) selectQuery += ", ";
    }
    selectQuery += " FROM storage WHERE key = ?;";

    sqlite3_stmt *selectStmt;
    opCheck = sqlite3_prepare_v2(db, selectQuery.c_str(), -1, &selectStmt, nullptr);

    if (opCheck != SQLITE_OK){
        std::cerr << "Prepare select failed: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return;
    }

    sqlite3_bind_int(selectStmt, 1, key);

    int emptyColumn = -1;
    if (sqlite3_step(selectStmt) == SQLITE_ROW){
        for (int i = 0; i < 49; ++i){ 
            const unsigned char *val = sqlite3_column_text(selectStmt, i);
            if (!val){
                emptyColumn = i + 2;
                break;
            }
        }
    }

    sqlite3_finalize(selectStmt);

    if (emptyColumn == -1) {
        std::cerr << "No empty column found for key " << key << std::endl;
        sqlite3_close(db);
        return;
    }

    std::string updateQuery = "UPDATE storage SET hexaDecValue" + std::to_string(emptyColumn) + " = ? WHERE key = ?;";
    sqlite3_stmt *updateStmt;

    opCheck = sqlite3_prepare_v2(db, updateQuery.c_str(), -1, &updateStmt, nullptr);
    if (opCheck != SQLITE_OK) {
        std::cerr << "Prepare update failed: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return;
    }

    sqlite3_bind_text(updateStmt, 1, hexaDecValue.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_int(updateStmt, 2, key);

    opCheck = sqlite3_step(updateStmt);

    if (opCheck != SQLITE_DONE){
        std::cerr << "Execution Error: " << sqlite3_errmsg(db) << std::endl;
    }
    else{
        std::cout << "Row updated in hexaDecValue" << emptyColumn << "!\n";
    }

    sqlite3_finalize(updateStmt);
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

        //Call funtions here;
        
        Py_DECREF(pModule);
    } 
    else {
        std::cerr << "Error: Could not import Python module." << std::endl;
        PyErr_Print();
    }

    Py_Finalize();
    return 0;
}
