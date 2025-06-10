#!/bin/bash
# Create a tar.gz archive of the project for safekeeping
ARCHIVE=who_are_you_backup.tar.gz
tar czf "$ARCHIVE" --exclude="$ARCHIVE" .
echo "Backup created: $ARCHIVE"
