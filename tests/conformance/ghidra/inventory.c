#include <stdio.h>

volatile int hurea_ghidra_inventory_global = 7;

enum HureaFixtureState { HUREA_FIXTURE_IDLE = 0, HUREA_FIXTURE_READY = 3 };
union HureaFixturePayload { unsigned int word; unsigned char bytes[4]; };
struct HureaFixtureLayout {
  enum HureaFixtureState state;
  union HureaFixturePayload payload;
  struct HureaFixtureLayout *next;
};
volatile struct HureaFixtureLayout hurea_ghidra_inventory_layout = {
    HUREA_FIXTURE_READY, {.word = 5}, 0};

__attribute__((noinline, used)) int hurea_ghidra_inventory_leaf(int value) {
  puts("HUREA_GHIDRA_LEAF_VALUE");
  return value + hurea_ghidra_inventory_global;
}

__attribute__((noinline, used)) int hurea_ghidra_inventory_branch(int value) {
  if (value > 10) {
    return hurea_ghidra_inventory_leaf(value);
  }
  return hurea_ghidra_inventory_leaf(-value);
}

__attribute__((noinline, used)) int hurea_ghidra_inventory_indirect(
    int (*callback)(int), int value) {
  return callback(value);
}

__attribute__((noinline, used)) int hurea_ghidra_inventory_switch(
    unsigned int selector, int value) {
  switch (selector) {
    case 0:
      return hurea_ghidra_inventory_leaf(value);
    case 1:
      return hurea_ghidra_inventory_leaf(value + 3);
    case 2:
      return hurea_ghidra_inventory_leaf(value - 5);
    case 3:
      return hurea_ghidra_inventory_leaf(value * 2);
    case 4:
      return hurea_ghidra_inventory_leaf(value ^ 0x55);
    case 5:
      return hurea_ghidra_inventory_leaf(value | 0x20);
    case 6:
      return hurea_ghidra_inventory_leaf(value & 0x3f);
    case 7:
      return hurea_ghidra_inventory_leaf(value + hurea_ghidra_inventory_global);
    default:
      return -1;
  }
}

__attribute__((noinline, used)) int hurea_ghidra_inventory_dense_switch(
    unsigned int selector, int value) {
  switch (selector) {
    case 0: return hurea_ghidra_inventory_leaf(value + 0);
    case 1: return hurea_ghidra_inventory_leaf(value + 1);
    case 2: return hurea_ghidra_inventory_leaf(value + 2);
    case 3: return hurea_ghidra_inventory_leaf(value + 3);
    case 4: return hurea_ghidra_inventory_leaf(value + 4);
    case 5: return hurea_ghidra_inventory_leaf(value + 5);
    case 6: return hurea_ghidra_inventory_leaf(value + 6);
    case 7: return hurea_ghidra_inventory_leaf(value + 7);
    case 8: return hurea_ghidra_inventory_leaf(value + 8);
    case 9: return hurea_ghidra_inventory_leaf(value + 9);
    case 10: return hurea_ghidra_inventory_leaf(value + 10);
    case 11: return hurea_ghidra_inventory_leaf(value + 11);
    case 12: return hurea_ghidra_inventory_leaf(value + 12);
    case 13: return hurea_ghidra_inventory_leaf(value + 13);
    case 14: return hurea_ghidra_inventory_leaf(value + 14);
    case 15: return hurea_ghidra_inventory_leaf(value + 15);
    case 16: return hurea_ghidra_inventory_leaf(value + 16);
    case 17: return hurea_ghidra_inventory_leaf(value + 17);
    case 18: return hurea_ghidra_inventory_leaf(value + 18);
    case 19: return hurea_ghidra_inventory_leaf(value + 19);
    case 20: return hurea_ghidra_inventory_leaf(value + 20);
    case 21: return hurea_ghidra_inventory_leaf(value + 21);
    case 22: return hurea_ghidra_inventory_leaf(value + 22);
    case 23: return hurea_ghidra_inventory_leaf(value + 23);
    case 24: return hurea_ghidra_inventory_leaf(value + 24);
    case 25: return hurea_ghidra_inventory_leaf(value + 25);
    case 26: return hurea_ghidra_inventory_leaf(value + 26);
    case 27: return hurea_ghidra_inventory_leaf(value + 27);
    case 28: return hurea_ghidra_inventory_leaf(value + 28);
    case 29: return hurea_ghidra_inventory_leaf(value + 29);
    case 30: return hurea_ghidra_inventory_leaf(value + 30);
    case 31: return hurea_ghidra_inventory_leaf(value + 31);
    case 32: return hurea_ghidra_inventory_leaf(value + 32);
    case 33: return hurea_ghidra_inventory_leaf(value + 33);
    case 34: return hurea_ghidra_inventory_leaf(value + 34);
    case 35: return hurea_ghidra_inventory_leaf(value + 35);
    case 36: return hurea_ghidra_inventory_leaf(value + 36);
    case 37: return hurea_ghidra_inventory_leaf(value + 37);
    case 38: return hurea_ghidra_inventory_leaf(value + 38);
    case 39: return hurea_ghidra_inventory_leaf(value + 39);
    default: return -1;
  }
}

__attribute__((noinline, used)) int hurea_ghidra_inventory_entry(void) {
  puts("HUREA_GHIDRA_INVENTORY_ENTRY");
  return hurea_ghidra_inventory_branch(35) +
         hurea_ghidra_inventory_indirect(hurea_ghidra_inventory_leaf, 0) +
         hurea_ghidra_inventory_dense_switch(100, 0) + 1;
}

int main(void) { return hurea_ghidra_inventory_entry() == 49 ? 0 : 1; }
