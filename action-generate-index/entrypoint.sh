#!/bin/bash
echo "Creating GH Pages deployment bundle…"

HTTP="/"
OUTPUT="site-index.html" 

i=0
echo "<UL>" > $OUTPUT
for filepath in `find "$INPUT_ROOT_DIR" -maxdepth 1 -mindepth 1 -type d| sort`; do
  path=`basename "$filepath"`
  echo "  <LI>$path</LI>" >> $OUTPUT
  echo "  <UL>" >> $OUTPUT
  for i in `find "$filepath" -maxdepth 1 -mindepth 1 -type f| sort`; do
    file=`basename "$i"`
    echo "    <LI><a href=\"/$path/$file\">$file</a></LI>" >> $OUTPUT
  done
  echo "  </UL>" >> $OUTPUT
done
echo "</UL>" >> $OUTPUT

echo "Done!"
