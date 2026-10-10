#include <stdio.h>
__attribute__((noinline, used)) int hurea_version_leaf(void) {
  puts("HUREA_VERSION_TWO");
  return 2;
}
__attribute__((noinline, used)) int hurea_added(void) { return 40; }
__attribute__((noinline, used)) int hurea_version_entry(void) {
  return hurea_version_leaf() + hurea_added();
}
int main(void) { return hurea_version_entry() == 42 ? 0 : 1; }
