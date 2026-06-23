#include <iostream>
#include <string>
#include <iomanip>
#include <bitset>
using namespace std;

int main(int argc, char* argv[]){
	if(argc<2){
		cerr << "Insufficient arguments!";
	} else if(argc>2){
	  	cerr << "Too many arguments!";
	} else {
		string pro(argv[1]);
		for(unsigned int i=0;i<pro.length();i++){
			cout << static_cast<unsigned int>(pro[i]) << " ";
		}
		cout << endl << hex;
		for(unsigned int i=0;i<pro.length();i++){
			cout << static_cast<unsigned int>(pro[i]) << " ";
		}
		cout << endl << dec;
		for(unsigned int i=0;i<pro.length();i++){
			cout << bitset<8>(pro[i]) << " ";
		}
	}
}
