/* from http://www.programmingsimplified.com/cpp/source-code/cpp-class-example-program */

#include<iostream>
 
using namespace std;
 
class programming
{
   private:
      int variable;
 
   public:
 
      void input_value()
      {
         cout << "In function input_value, Enter an integer\n";
         cin >> variable;
      }
 
      void output_value()
      {
         cout << "Variable entered is ";
         cout << variable << "\n";
      }
};
 
main()
{
   programming object;
 
   object.input_value();
   object.output_value();
 
   //object.variable;  Will produce an error because variable is private
 
   return 0;
}
