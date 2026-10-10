typedef int (*hurea_cross_callback)(int);

volatile int hurea_cross_global = 7;
const volatile char hurea_cross_message[] = "HUREA_GHIDRA_CROSS_FORMAT";

__attribute__((noinline, used)) int hurea_cross_leaf(int value) {
  return value + hurea_cross_global + hurea_cross_message[0] - 'R';
}

__attribute__((noinline, used)) int hurea_cross_branch(int value) {
  if (value > 10) {
    return hurea_cross_leaf(value);
  }
  return hurea_cross_leaf(-value);
}

__attribute__((noinline, used)) int hurea_cross_indirect(
    hurea_cross_callback callback, int value) {
  return callback(value);
}

#define HUREA_CROSS_SWITCH_CASE(case_value) \
  case case_value:                        \
    return hurea_cross_leaf(payload + case_value)

__attribute__((noinline, used)) int hurea_cross_dense_switch(unsigned int selector,
                                                           int payload) {
  switch (selector) {
    HUREA_CROSS_SWITCH_CASE(0);
    HUREA_CROSS_SWITCH_CASE(1);
    HUREA_CROSS_SWITCH_CASE(2);
    HUREA_CROSS_SWITCH_CASE(3);
    HUREA_CROSS_SWITCH_CASE(4);
    HUREA_CROSS_SWITCH_CASE(5);
    HUREA_CROSS_SWITCH_CASE(6);
    HUREA_CROSS_SWITCH_CASE(7);
    HUREA_CROSS_SWITCH_CASE(8);
    HUREA_CROSS_SWITCH_CASE(9);
    HUREA_CROSS_SWITCH_CASE(10);
    HUREA_CROSS_SWITCH_CASE(11);
    HUREA_CROSS_SWITCH_CASE(12);
    HUREA_CROSS_SWITCH_CASE(13);
    HUREA_CROSS_SWITCH_CASE(14);
    HUREA_CROSS_SWITCH_CASE(15);
    HUREA_CROSS_SWITCH_CASE(16);
    HUREA_CROSS_SWITCH_CASE(17);
    HUREA_CROSS_SWITCH_CASE(18);
    HUREA_CROSS_SWITCH_CASE(19);
    HUREA_CROSS_SWITCH_CASE(20);
    HUREA_CROSS_SWITCH_CASE(21);
    HUREA_CROSS_SWITCH_CASE(22);
    HUREA_CROSS_SWITCH_CASE(23);
    HUREA_CROSS_SWITCH_CASE(24);
    HUREA_CROSS_SWITCH_CASE(25);
    HUREA_CROSS_SWITCH_CASE(26);
    HUREA_CROSS_SWITCH_CASE(27);
    HUREA_CROSS_SWITCH_CASE(28);
    HUREA_CROSS_SWITCH_CASE(29);
    HUREA_CROSS_SWITCH_CASE(30);
    HUREA_CROSS_SWITCH_CASE(31);
    HUREA_CROSS_SWITCH_CASE(32);
    HUREA_CROSS_SWITCH_CASE(33);
    HUREA_CROSS_SWITCH_CASE(34);
    HUREA_CROSS_SWITCH_CASE(35);
    HUREA_CROSS_SWITCH_CASE(36);
    HUREA_CROSS_SWITCH_CASE(37);
    HUREA_CROSS_SWITCH_CASE(38);
    HUREA_CROSS_SWITCH_CASE(39);
    default:
      return -1;
  }
}

#undef HUREA_CROSS_SWITCH_CASE

__attribute__((noinline, used, visibility("default"))) int hurea_cross_entry(void) {
  return hurea_cross_branch(35) + hurea_cross_indirect(hurea_cross_leaf, 0);
}

__attribute__((used, visibility("default"))) void hurea_cross_start(void) {
  volatile int result = hurea_cross_entry();
  (void)result;
  for (;;) {
  }
}
