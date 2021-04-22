build() {
    # macOS SIP swallows DYLD_LIBRARY_PATH so export the duplicate in
    # LSST_LIBRARY_PATH
    if [[ -z $DYLD_LIBRARY_PATH ]]; then
        export DYLD_LIBRARY_PATH=$LSST_LIBRARY_PATH
    fi
    stack-docs build
}
