#include <stdio.h>

volatile int hurea_c_global = 7;

__attribute__((noinline, used)) int hurea_leaf(int value) {
  puts("HUREA_C_LEAF");
  return value + hurea_c_global;
}

__attribute__((noinline, used)) int hurea_branch(int value) {
  return value > 3 ? hurea_leaf(value) : hurea_leaf(-value);
}

__attribute__((noinline, used)) int hurea_entry(void) {
  puts("HUREA_C_ENTRY");
  return hurea_branch(5);
}

int main(void) { return hurea_entry() == 12 ? 0 : 1; }
