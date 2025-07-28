#include <sqlite3.h>
#include <iostream>
#include <sstream>

int main() {
    std::string dbName = "NewsStorage/storage.db";
    sqlite3* db;
    int rc = sqlite3_open(dbName.c_str(), &db);
    
    if (rc != SQLITE_OK) {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        return 0;
    }

    std::ostringstream createTableSQL;
    createTableSQL << "CREATE TABLE IF NOT EXISTS storage (key TEXT PRIMARY KEY";

    for (int i = 1; i <= 50; ++i) {
        createTableSQL << ", hexaDecValue" << i << " TEXT";
    }

    createTableSQL << ");";

    char* errMsg = nullptr;
    rc = sqlite3_exec(db, createTableSQL.str().c_str(), nullptr, nullptr, &errMsg);

    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << errMsg << std::endl;
        sqlite3_free(errMsg);
    } else {
        std::cout << "Database created successfully with 50 columns." << std::endl;
    }

    sqlite3_close(db);
}
