SUBDIRS="D206_Wärmepumpe_withTemplate"
set -e
for dir in ${SUBDIRS}; do
    echo "Now making ${dir}"
    make -C ${dir};
done
