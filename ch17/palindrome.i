%module palindrome

%{
#include <string.h>
%}

%inline %{
extern int is_palindrome(char *text);
%}
