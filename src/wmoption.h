#ifndef __WMOPTION_H
#define __WMOPTION_H

#include "upath.h"
#include "yarray.h"
#include "ypointer.h"

struct WindowOption {
    WindowOption(ustring n_class_instance = null);
    void combine(const WindowOption& n);

    ustring w_class_instance;
    ustring keyboard;
    ustring icon;
    unsigned functions, function_mask;
    unsigned decors, decor_mask;
    unsigned options, option_mask;
    int workspace;
    int layer;
    int tray;
    int order;
    int opacity;
    int gflags;
    int gx, gy;
    unsigned gw, gh;
};

class WindowOptions {
public:
    void setWinOption(ustring n_class_instance,
                      const char *opt, const char *arg);

    void mergeWindowOption(WindowOption &cm,
                           ustring a_class_instance,
                           bool remove);

    int getCount() const { return fWinOptions.getCount(); }
    bool nonempty() const { return getCount(); }
    bool isEmpty() const { return !getCount(); }

private:
    YObjectArray<WindowOption> fWinOptions;

    bool findOption(ustring a_class_instance, int *index);

    WindowOption *getOption(ustring a_class_instance);
};

extern lazy<WindowOptions> defOptions;
extern lazy<WindowOptions> hintOptions;

void loadWinOptions(upath optFile);

#endif

// vim: set sw=4 ts=4 et:
