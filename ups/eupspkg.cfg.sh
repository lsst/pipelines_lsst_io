build() {
    # macOS SIP swallows DYLD_LIBRARY_PATH so export the duplicate in
    # LSST_LIBRARY_PATH
    if [[ -z $DYLD_LIBRARY_PATH ]]; then
        export DYLD_LIBRARY_PATH=$LSST_LIBRARY_PATH
    fi
    stack-docs build
}

install() {
    clean_old_install
    mkdir -p "$PREFIX"
    cp -a \
        _build.log \
        _build.sh \
        _build.tags \
        conf.py \
        COPYRIGHT \
        LICENSE \
        README.md "$PREFIX"
    cd "$reldir"
    if [[ -d "ups" && ! -d "$PREFIX/ups" ]]; then
        install_ups
    fi
}
