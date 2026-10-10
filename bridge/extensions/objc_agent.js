// Compile explicitly in a project containing frida-objc-bridge and frida-compile.
import ObjC from "frida-objc-bridge";
let events = 0;
rpc.exports = {
  start(parameters) {
    if (!ObjC.available) throw new Error("Objective-C runtime unavailable");
    const klass = ObjC.classes[parameters.class];
    if (klass === undefined) throw new Error("Objective-C class unavailable");
    const method = klass[parameters.selector];
    if (method === undefined)
      throw new Error("Objective-C selector unavailable");
    const cap = parameters.max_events || 1000;
    const emit = (value) => {
      if (events++ < cap) send(value);
    };
    Interceptor.attach(method.implementation, {
      onEnter(args) {
        emit({
          event: "objc_enter",
          class: parameters.class,
          selector: parameters.selector,
          thread: Process.getCurrentThreadId(),
          argument_pointers: [0, 1, 2, 3].map((i) => args[i].toString()),
          backtrace: Thread.backtrace(this.context, Backtracer.ACCURATE).map(
            (x) => DebugSymbol.fromAddress(x).toString(),
          ),
        });
      },
      onLeave(value) {
        emit({
          event: "objc_leave",
          return_pointer: value.toString(),
          thread: Process.getCurrentThreadId(),
        });
      },
    });
    emit({ event: "ready" });
  },
};
