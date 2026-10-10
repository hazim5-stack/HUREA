#include <stdio.h>
__attribute__((noinline, used)) int hurea_version_leaf(void) {
  puts("HUREA_VERSION_ONE");
  return 1;
}
__attribute__((noinline, used)) int hurea_version_entry(void) {
  return hurea_version_leaf();
}
int main(void) { return hurea_version_entry() == 1 ? 0 : 1; }
