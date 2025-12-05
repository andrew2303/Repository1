#include <iostream>
using namespace std;

int main() {
  int num;
  cout << "How many numbers? " << endl;
  cin >> num;

  for (int i = 0; i < num; i++) {
    cout << i << endl;
  }
  
  return 0;
}
