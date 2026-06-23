#include <iostream>
#include <fstream>
#include <string>
#include <random>
#include <cstdint>
#include <limits>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <file>\n";
        return 1;
    }

    const std::string filepath = argv[1];

    // Open file for reading and writing in binary mode
    std::fstream file(filepath, std::ios::in | std::ios::out | std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file \"" << filepath << "\"\n";
        return 1;
    }

    // Determine file size
    file.seekg(0, std::ios::end);
    const std::streamoff fileSize = file.tellg();
    file.seekg(0, std::ios::beg);

    std::cout << "File: " << filepath << "\n";
    std::cout << "File size: " << fileSize << " bytes\n\n";

    // --- Address range input ---
    std::streamoff startAddr = 0, endAddr = 0;

    std::cout << "Enter start address (byte offset, 0-based, max " << fileSize - 1 << "): ";
    std::cin >> startAddr;

    std::cout << "Enter end address   (byte offset, inclusive,  max " << fileSize - 1 << "): ";
    std::cin >> endAddr;

    if (std::cin.fail() || startAddr < 0 || endAddr < startAddr || endAddr >= fileSize) {
        std::cerr << "Error: Invalid address range ["
                  << startAddr << ", " << endAddr << "] for file of size " << fileSize << "\n";
        return 1;
    }

    // --- Byte value range input ---
    int byteMin = 0, byteMax = 0;

    std::cout << "Enter minimum byte value (0-255): ";
    std::cin >> byteMin;

    std::cout << "Enter maximum byte value (0-255): ";
    std::cin >> byteMax;

    if (std::cin.fail() || byteMin < 0 || byteMax > 255 || byteMin > byteMax) {
        std::cerr << "Error: Invalid byte range [" << byteMin << ", " << byteMax << "]\n";
        return 1;
    }

    // --- Write random bytes ---
    std::random_device rd;
    std::mt19937 rng(rd());
    std::uniform_int_distribution<int> dist(byteMin, byteMax);

    const std::streamoff regionLen = endAddr - startAddr + 1;

    file.seekp(startAddr, std::ios::beg);
    if (file.fail()) {
        std::cerr << "Error: Failed to seek to offset " << startAddr << "\n";
        return 1;
    }

    for (std::streamoff i = 0; i < regionLen; ++i) {
        const char byte = static_cast<char>(dist(rng));
        file.write(&byte, 1);
        if (file.fail()) {
            std::cerr << "Error: Write failed at offset " << (startAddr + i) << "\n";
            return 1;
        }
    }

    file.flush();
    file.close();

    std::cout << "\nDone. Overwrote " << regionLen << " byte(s) at offsets ["
              << startAddr << ", " << endAddr << "] "
              << "with random values in [" << byteMin << ", " << byteMax << "].\n";

    return 0;
}