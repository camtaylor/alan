#include<iostream>

using namespace std;

int main()
{
   int n, c, first = 0, second = 1, next;

   cout << ":speak:Enter the number of terms of Fibonacci series you want" << endl;
   cout << ":listen:" << endl;
   cin >> n;

   cout << ":speak:First " << n << " terms of Fibonacci series are :- " << endl;

   for ( c = 0 ; c < n ; c++ )
   {
      if ( c <= 1 )
         next = c;
      else
      {
         next = first + second;
         first = second;
         second = next;
      }
      cout << ":speak:" << next << endl;
   }

   return 0;
}
